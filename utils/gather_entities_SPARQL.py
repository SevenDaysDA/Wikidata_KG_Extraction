import requests
import json


import rdflib


def get_entity_by_name(name):
    '''
    name - The name of the preferred label
    Return - List of all entites, which are found for the given name entity.
    '''

    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = ''' SELECT ?item ?prefLabel
        WHERE {
            values ?prefLabel {"'''+str(name)+'''"@en}
            ?item rdfs:label|skos:altLabel ?prefLabel.
        }'''
    response = requests.get(url, params={'query': query, 'format': 'json'}).json()
    result = []
    for res in response['results']['bindings']:
        result.append(res['item']['value'])
    return result
    
# Help class
def json_to_doubles(data):
    result = []
    for a in data['results']['bindings']:
        result.append((a['relation']['value'], a['obj']['value']))
    return result

def get_outgoing_nodes(entity_id):
    '''
    entity_id - Wikidata id for entity
    '''
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = '''select ?relation ?obj where { wd:''' + str(entity_id) + ''' ?relation ?obj }'''
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    
    return json_to_doubles(data)


def get_Subgraph(entity_id):
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = '''select ?relation ?obj 
    where { wd:'''+str(entity_id)+''' ?relation ?obj .
        ?obj ?relation2 ?obj2 }'''
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    return json_to_doubles(data)