# THESE Methods are depreceated

#  need this !pip install rdflib
from rdflib import Graph
import rdflib
import requests





def get_subgraph_sub(parent_entity_id, graph_temp, hops):
  local_entity_graph = Graph()
  local_leaf_graph = Graph()
  if hops > 0:
    graph = Graph()
    graph.parse(f"https://www.wikidata.org/wiki/Special:EntityData/{parent_entity_id}.nt")
    for a in graph.triples((rdflib.term.URIRef(f'http://www.wikidata.org/entity/{parent_entity_id}'), None, None)):
      if "http://www.wikidata.org/prop" in str(a[1]) and "http://www.wikidata.org/entity/Q" in str(a[2]) and not "-" in str(a[2]):
        local_entity_graph.add(a)
        if hops > 0:
          id = str(a[2]).split("Q")
          ents, leafs = get_subgraph_sub(f"Q{id[1]}", graph_temp, hops-1)
          for aid in ents:
            local_entity_graph.add(aid)
          for leaf in leafs:
            local_leaf_graph.add(leaf)

      elif "http://www.wikidata.org/prop" in str(a[1]) and not "-" in str(a[2]):
        # This is only leaf with value
        local_leaf_graph.add(a)

  return local_entity_graph, local_leaf_graph

def get_subgraph(parent_entity_id, hops):
  start_graph = Graph()
  return get_subgraph_sub(parent_entity_id, start_graph, hops)