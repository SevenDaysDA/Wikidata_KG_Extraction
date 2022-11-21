from utils.gather_entities import get_subgraph
from utils.gather_entities_SPARQL import *


result = get_entity_by_name("Barack Obama")

print(result)

result = get_outgoing_nodes("Q76")
for res in result:
    print(res)

