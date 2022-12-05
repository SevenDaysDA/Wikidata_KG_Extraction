# from utils.gather_entities import get_subgraph
from utils.gather_entities_SPARQL import *



# tasks = ['ent_by_name', 'outgoing_nodes', 'subgraph', 'edges]
tasks = ['edges']

if 'ent_by_name' in tasks:
    result = get_entity_by_name("Barack Obama") # res -> ['http://www.wikidata.org/entity/Q76', 'http://www.wikidata.org/entity/Q47513588', 'http://www.wikidata.org/entity/Q61909968']
    print(result)

if 'outgoing_nodes' in tasks:
    result = get_outgoing_nodes("Q76")          # res -> [('http://www.wikidata.org/prop/direct/P3368', '727223'), ('http://www.wikidata.org/prop/direct/P3373', 'http://www.wikidata.org/entity/Q773197'), ('http://www.wikidata.org/prop/direct/P3373', 'http://www.wikidata.org/entity/Q4382677')
    print(len(result))                          # 1428
if 'subgraph' in tasks:
    result = clean_hyperlinks(get_Subgraph("Q76"), True)    
    for a in result:
        print(a)
    print(len(result))
 
if 'edges' in tasks:
    result = get_edges_from_id("Q30")
    print(result)