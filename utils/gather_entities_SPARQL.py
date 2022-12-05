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
                                # BUG: MAYBE TO BIG
        for value in line.values():
            value_line += (value['value'],)
        result.append(value_line)
        # print(value_line)

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


def get_edges_from_id(entity_id):
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

    query = '''SELECT ?wd ?wdLabel ?p ?ps_ ?ps_Label ?wdpqLabel ?pq_Label{
  VALUES (?company) {(wd:'''+str(entity_id)+''')}
  
  ?company ?p ?statement .
  ?statement ?ps ?ps_ .
  
  ?wd wikibase:claim ?p.
  ?wd wikibase:statementProperty ?ps.
  
  OPTIONAL {
  ?statement ?pq ?pq_ .
  ?wdpq wikibase:qualifier ?pq .
  }

  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} ORDER BY ?wd ?statement ?ps_'''

    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    return set(__json_to_doubles(data))


def get_edge_for_nodepair(entity_one, entity_two):
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

    query = '''SELECT ?wd ?wdLabel ?p ?ps_ ?ps_Label ?wdpqLabel ?pq_Label{
  VALUES (?company) {(wd:'''+str(entity_one)+''')}
  
  ?company ?p ?statement .
  ?statement ?ps ?ps_ .
  
  ?wd wikibase:claim ?p.
  ?wd wikibase:statementProperty ?ps.
  
  OPTIONAL {
  ?statement ?pq ?pq_ .
  ?wdpq wikibase:qualifier ?pq .
  }

  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} ORDER BY ?wd ?statement ?ps_'''
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    response_clean =  set(__json_to_doubles(data))
    # for line in response_clean:

    result = []
    for line in response_clean:
        if entity_two in line[2][-len(entity_two):]:    #Maybe filtering to many out, what happens to statements?
            result.append(line)
    return result


def predicate_by_property(entity_id, property_id):
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = '''SELECT ?item ?itemLabel 
WHERE 
{ wd:'''+str(entity_id)+ ''' wdt:''' + str(property_id)+''' ?item. 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # <span lang="en" dir="ltr" class="mw-content-ltr">Helps get the label in your language, if not, then en language</span>
}'''
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    response_clean =  set(__json_to_doubles(data))
    return response_clean

def posticate_by_property(property_id, entity_id):
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = '''SELECT ?item ?itemLabel 
WHERE 
{ ?item wdt:''' + str(property_id)+''' wd:'''+str(entity_id)+ ''' . 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # <span lang="en" dir="ltr" class="mw-content-ltr">Helps get the label in your language, if not, then en language</span>
}'''
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    print(data)
    response_clean =  set(__json_to_doubles(data))
    return response_clean