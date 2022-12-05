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
    
    
###########################   Help class   ###########################
def clean_hyperlinks_old(data, Delete_BoxID = True):
    result = []
    for i in data:
        prefixes = ["http://www.wikidata.org/entity/statement/", "http://www.wikidata.org/prop/"]
        clean_tuple = ()
        for i_element in i:
            # Replace if prefix appears
            for prefix in prefixes:
                if prefix in i_element:
                    clean_tuple += (i_element.split('-')[0].replace(prefix, "") ,) if Delete_BoxID and "-" in i_element else (i_element.replace(prefix, "") ,)
        result.append(clean_tuple)
    return set(result)

def clean_hyperlinks_old_old(data, Delete_BoxID = True):
    prefixes = ["http://www.wikidata.org/entity/", "http://www.wikidata.org/prop/", "direct/", "statement/"]
    result = []

    for i in data:
        clean_tuple = ()
        for i_element in i:
            local = i_element
            # Replace if prefix appears
            for prefix in prefixes:
                if prefix in local:
                    local = local.split(prefix)[1]
                if Delete_BoxID and '-' in local:
                    local = local.split('-')[0]
            clean_tuple += (local,)
        result.append(clean_tuple)
    return set(result)       # set()

def clean_hyperlinks(data, Delete_BoxID = True):
    prefixes = ["http://www.wikidata.org/entity/", "http://www.wikidata.org/prop/", "direct/", "statement/"]
    result = []

    for i in data:
        clean_tuple = ()
        skip_tuple = False
        for i_element in i:
            if Delete_BoxID and '-' in i_element:
                skip_tuple = True
                continue
            local = i_element
            # Replace if prefix appears
            for prefix in prefixes:
                if prefix in local:
                    local = local.split(prefix)[1]
            clean_tuple += (local,)
        if not skip_tuple:
            result.append(clean_tuple)
    return result       # set()
        

def __json_to_doubles(data):
    result = []
    for line in data['results']['bindings']:
        value_line=()
        print(line)                         # BUG: MAYBE TO BIG
        for value in line.values():
            value_line += (value['value'],)
        result.append(value)
    return result

######################################################################

def get_outgoing_nodes(entity_id):
    '''
    entity_id - Wikidata id for entity
    '''
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = '''select ?relation ?obj where { wd:''' + str(entity_id) + ''' ?relation ?obj }'''
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    
    return __json_to_doubles(data)


def get_Subgraph(entity_id, hops=2):
    # TODO: composing wit new loops
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'


    query = '''select ''' + ' '.join(["?relation"+str(hop)+" ?obj"+str(hop) for hop in range(hops)]) + ''' where { wd:'''+str(entity_id)+" ?relation0 ?obj0 . " + ' . '.join(["?obj"+str(hop) +" ?relation"+str(hop+1)+" ?obj"+str(hop+1) for hop in range(hops-1)])+''' }'''

    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    return set(__json_to_doubles(data))