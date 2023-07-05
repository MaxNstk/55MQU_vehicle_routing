import statistics
from iterated_greedy import IteratedGreedyCRVP

from semi_greedy import SemiGreedyCRVP
from simple_local_search import SimpleLocalSearch

#from simple_local_search import SimpleLocalSearch

# from iterated_greedy import IteratedGreedyCRVP

instances = [
    "instances/A/A-n32-k5.vrp",
    "instances/A/A-n33-k6.vrp",
    "instances/A/A-n37-k5.vrp",
    "instances/A/A-n39-k5.vrp",
    "instances/A/A-n44-k6.vrp",
    "instances/A/A-n45-k7.vrp",
    "instances/A/A-n46-k7.vrp",
    "instances/A/A-n48-k7.vrp",
    "instances/A/A-n53-k7.vrp",
    "instances/A/A-n54-k7.vrp",
    "instances/A/A-n60-k9.vrp",
    "instances/A/A-n62-k8.vrp",
    "instances/A/A-n63-k10.vrp",
    "instances/A/A-n63-k9.vrp",
    "instances/A/A-n65-k9.vrp",
    "instances/A/A-n80-k10.vrp"
]

'''
semy_greedy_results = []
for instance in instances:
    semi_greedy = SemiGreedyCRVP(file_path=instance,k_percentage=15)
    results = semi_greedy.run()
    
    print(instance," :",results["optimal_cost"]," - ",results["solution_cost"]," - ",results["optimal_cost"]/results["solution_cost"])
    
    semy_greedy_results.append(results["optimal_cost"]/results["solution_cost"])

print(sum(semy_greedy_results) / len(semy_greedy_results))
'''

'''
iterated_greedy_results = []
for instance in instances:
    iterated_greedy = IteratedGreedyCRVP(file_path=instance, max_iterations=5000, destruction_percentage=70, k_percentage=15)
    results = iterated_greedy.run()

    print(instance," :",results["optimal_cost"]," - ",results["solution_cost"]," - ",results["optimal_cost"]/results["solution_cost"]," - ",results["routes"])

    iterated_greedy_results.append(results["optimal_cost"]/results["solution_cost"])

print(sum(iterated_greedy_results) / len(iterated_greedy_results))   
'''

simple_local_search_results = []
for instance in instances:
    simple_local_search = SimpleLocalSearch(file_path=instance,max_iterations=40)
    results = simple_local_search.run()

    print(instance," :",results["optimal_cost"]," - ",results["solution_cost"]," - ",results["optimal_cost"]/results["solution_cost"])

    simple_local_search_results.append(results["optimal_cost"]/results["solution_cost"])

print(sum(simple_local_search_results) / len(simple_local_search_results)) 



#iterated_greedy = IteratedGreedyCRVP(file_path="instances\A\A-n32-k5.vrp")
#print(iterated_greedy.run(max_iterations=5000, destruction_percentage=20))

#simple_local_search = SimpleLocalSearch('instances/A/A-n80-k10.vrp')
#print(simple_local_search.run(5000))
