# from utils.gather_entities import get_subgraph
from utils.gather_entities_SPARQL import *


result = get_entity_by_name("Barack Obama") # res -> ['http://www.wikidata.org/entity/Q76', 'http://www.wikidata.org/entity/Q47513588', 'http://www.wikidata.org/entity/Q61909968']
print(result)

result = get_outgoing_nodes("Q76")          # res -> [('http://www.wikidata.org/prop/direct/P3368', '727223'), ('http://www.wikidata.org/prop/direct/P3373', 'http://www.wikidata.org/entity/Q773197'), ('http://www.wikidata.org/prop/direct/P3373', 'http://www.wikidata.org/entity/Q4382677')
print(len(result))                          # 1428

result = get_Subgraph("Q76")          # 
for a in result:
    print(a)
