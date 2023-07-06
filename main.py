import statistics
from grasp_iterated_greedy import GRASPIteratedGreedyCRVP
from grasp_local_search import GRASPLocalSearch
from iterated_greedy import IteratedGreedyCRVP
from iterated_local_search import IteratedLocalSearch

from semi_greedy import SemiGreedyCRVP
from simple_local_search import SimpleLocalSearch

#from simple_local_search import SimpleLocalSearch

# from iterated_greedy import IteratedGreedyCRVP

instances = [
    "instances/A/A-n32-k5.vrp"
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

'''
simple_local_search_results = []
for instance in instances:
    simple_local_search = SimpleLocalSearch(file_path=instance,max_iterations=100)
    results = simple_local_search.run()

    print(instance," :",results["optimal_cost"]," - ",results["solution_cost"]," - ",results["optimal_cost"]/results["solution_cost"])

    simple_local_search_results.append(results["optimal_cost"]/results["solution_cost"])

print(sum(simple_local_search_results) / len(simple_local_search_results)) 
'''

'''
iterated_local_search_results = []
for instance in instances:
    iterated_local_search = IteratedLocalSearch(file_path=instance,max_iterations=50, n_distortion=20)
    results = iterated_local_search.run()

    print(instance," :",results["optimal_cost"]," - ",results["solution_cost"]," - ",results["optimal_cost"]/results["solution_cost"])

    iterated_local_search_results.append(results["optimal_cost"]/results["solution_cost"])

print(sum(iterated_local_search_results) / len(iterated_local_search_results)) 
'''
'''
grasp_simple_local_search_results = []
for instance in instances:
    grasp_simple_local_search = GRASPLocalSearch(file_path=instance,max_iterations=100,k_percentage=15, internal_iterations=100)
    results = grasp_simple_local_search.run()

    print(instance," :",results["optimal_cost"]," - ",results["solution_cost"]," - ",results["optimal_cost"]/results["solution_cost"])

    grasp_simple_local_search_results.append(results["optimal_cost"]/results["solution_cost"])

print(sum(grasp_simple_local_search_results) / len(grasp_simple_local_search_results)) 
'''

grasp_iterated_local_search_results = []
for instance in instances:
    grasp_simple_local_search = GRASPIteratedGreedyCRVP(file_path=instance,max_iterations=5000, destruction_percentage=70, k_percentage=15,internal_iterations=1000)
    results = grasp_simple_local_search.run()

    print(instance," :",results["optimal_cost"]," - ",results["solution_cost"]," - ",results["optimal_cost"]/results["solution_cost"])

    grasp_iterated_local_search_results.append(results["optimal_cost"]/results["solution_cost"])

print(sum(grasp_iterated_local_search_results) / len(grasp_iterated_local_search_results)) 

#iterated_greedy = IteratedGreedyCRVP(file_path="instances\A\A-n32-k5.vrp")
#print(iterated_greedy.run(max_iterations=5000, destruction_percentage=20))

#simple_local_search = SimpleLocalSearch('instances/A/A-n80-k10.vrp')
#print(simple_local_search.run(5000))
