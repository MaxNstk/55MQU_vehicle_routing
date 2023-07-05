import random
import copy
from iterated_local_search import IteratedLocalSearch
from semi_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem

class GRASPIteratedLocalSearch(VehicleRoutingProblem):

    def __init__(self,max_iterations, k_percentage, internal_iterations, n_distorcion,  file_path="instances\A\A-n32-k5.vrp"):
        super().__init__(file_path)
        self.max_iterations = max_iterations
        self.internal_iterations = internal_iterations
        self.k_percentage = k_percentage
        self.n_distorcion = n_distorcion
        self.semi_greedy = SemiGreedyCRVP(k_percentage=k_percentage, file_path=self.file_path)
        
    # Função que implementa o algoritmo de busca local iterada
    def run(self):
        
        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while self.max_iterations > 0:

            #define solução inicial       
            initial_solution = self.semi_greedy.run()

            self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']

            iterated_local_search = IteratedLocalSearch(
                k_percentage=self.k_percentage, file_path=self.file_path, max_iterations=self.internal_iterations,
                n_distortion=self.n_distorcion).run(initial_solution=copy.deepcopy(self.current_routes))
            self.max_iterations -= self.internal_iterations
            
            if iterated_local_search['solution_cost'] == self.optimal_value:
                break

            if self.max_iterations < self.internal_iterations:
                self.internal_iterations = self.max_iterations

            self.current_routes, self.current_routes_cost = iterated_local_search['routes'], iterated_local_search['solution_cost']
            
            self.check_current_routes()

        return {
            'routes':self.best_routes,
            'solution_cost': round(self.best_cost, 2),
            'optimal_cost': self.optimal_value,
            'max_iterations': self.max_iterations
        }

simple_iterated_local_search = GRASPIteratedLocalSearch(max_iterations=1000, k_percentage=15, internal_iterations=100, n_distorcion=2)
print(simple_iterated_local_search.run())
