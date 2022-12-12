import time
from utils.gather_entities import get_subgraph
from utils.gather_entities_SPARQL import *


start_time = time.time()

tasks = []

# tasks.append("request")
# tasks.append("SPARQL")
# tasks.append("names")
tasks.append("edge")


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

if "subgragphs" in  tasks:
    results = []
    roots = ["Q76", "Q31", "Q30"]
    # roots = ["Q76" for _ in range(5)]
    print("Request for : ")
    print(roots)
    print()
    temp_time = 0
    for root in roots:
        results.append(get_Subgraph(root, hops=2))
        temp_time = time.time() - temp_time - start_time
        print(round(temp_time,2))
    print()
    for res in results:
        print("Length of result: ",len(res))
    print("Measurement with SPARQL: ")


if "names" in tasks:
    if False:
        print("All single by single")
        names = ["Obama", "France", "President"]
        print("Names: ", names)

        results = []
        temp_time=0
        for name in names:
            results.append(get_entity_by_name(name))
            temp_time = time.time() - temp_time - start_time
            print(f"Time: {round(temp_time, 2)} sec for  \"{name} \" ")
        print("Results:")
        for res in results:
            print(len(res))
        end_time = time.time() - start_time
        print("Time needed: ", round(end_time, 2))

    if False:
        start_time = time.time()
        print("All together")
        # names = ["Obama", "France", "President"]
        names = ["Obama", "United States of America", "Japan", "France", "Germany", "Bush"]
        print("Names: ", names)


        results = get_entity_by_names(names)
        end_time = time.time() - start_time
        
        print("Results:")
        for res in results:
            print(len(res))
        print("Time needed: ", round(end_time, 2))

    # Benchmarking subgraphs
    start_time = time.time()
    print("All together")
    # names = ["Obama", "France", "President"]
    names = ["Q76", "Q30", "Q17"]
    print("Names: ", names)

    results = []
    for sub in names:
        results.append(get_Subgraph(sub, hops=1))

    end_time = time.time() - start_time
    
    print("Results:")
    for res in results:
        print(len(res))
    print("Time needed: ", round(end_time, 2))


if "edge" in tasks:
    query = ["Q76", "Q30", "Q17", "Q142", "Q183", "Q207"]
    response = get_edges_by_IDs(query)
    print(len(response["results"]["bindings"]))





print()
print("Final time end:")
end_time = time.time() - start_time
print("Time needed: ", round(end_time, 2))
