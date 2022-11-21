import time
from utils.gather_entities import get_subgraph
from utils.gather_entities_SPARQL import get_Subgraph


start_time = time.time()

tasks = []

# tasks.append("request")
tasks.append("SPARQL")


print("Starting measuring....")
print("------------------------------------------------------")
print()


if "request" in tasks:
    print("Measurements for page requests with rdf: ")
    graph3hop = get_subgraph("Q484652", 3)
    time_3hop = time.time() - start_time
    print("Time for 3 hops: ", round(time_3hop,1))
    graph2hop =  get_subgraph("Q484652", 2)
    time_2hop = time.time() - time_3hop - start_time
    print("Time for 2 hops: ", round(time_2hop, 1))

if "SPARQL" in  tasks:
    print("------------------------------------------------------")
    print()
    print("Measurement with SPARQL: ")







end_time = time.time() - start_time
