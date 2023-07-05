import random
import copy
from semi_greedy import SemiGreedyCRVP
from simple_local_search import SimpleLocalSearch
from vehicle_routing_problem import VehicleRoutingProblem

class IteratedLocalSearch(VehicleRoutingProblem):

    def __init__(self,max_iterations,internal_iterations, file_path="instances\A\A-n32-k5.vrp"):
        self.internal_iterations = internal_iterations
        self.max_iterations = max_iterations
        super().__init__(file_path)


    # Função que implementa o algoritmo de busca local simples
    def run(self):

        #define solução inicial
        initial_solution = SemiGreedyCRVP(k_percentage=20, file_path=self.file_path).run()

        self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']

        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while self.max_iterations > 0:

            local_search = SimpleLocalSearch(
                file_path=self.file_path, max_iterations=self.internal_iterations
                ).run(initial_solution=copy.deepcopy(self.current_routes))
            
            if local_search['solution_cost'] == self.optimal_value:
                break
            self.max_iterations -= (self.internal_iterations -local_search['remaining_iterations'])+1
            self.current_routes = local_search['routes']
            self.current_routes_cost = self.get_routes_cost(self.current_routes)


            if self.internal_iterations > self.max_iterations:
                self.internal_iterations = self.max_iterations

        return {
            'routes':self.current_routes,
            'solution_cost': round(self.current_routes_cost, 2),
            'optimal_cost': self.optimal_value,
            'max_iterations': self.max_iterations
        }

simple_local_search = IteratedLocalSearch(max_iterations=5000, internal_iterations=100)
print(simple_local_search.run())
