import copy
from semi_greedy import SemiGreedyCRVP
from simple_local_search import SimpleLocalSearch
from vehicle_routing_problem import VehicleRoutingProblem

class GRASPLocalSearch(VehicleRoutingProblem):

    def __init__(self,max_iterations, k_percentage, internal_iterations,  file_path="instances\A\A-n32-k5.vrp"):
        super().__init__(file_path)
        self.max_iterations = max_iterations
        self.internal_iterations = internal_iterations
        self.semi_greedy = SemiGreedyCRVP(k_percentage=k_percentage, file_path=self.file_path)
        
    # Função que implementa o algoritmo de busca local iterada
    def run(self):
        
        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while self.max_iterations > 0:

            #define solução inicial       
            initial_solution = self.semi_greedy.run()

            self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']

            local_search = SimpleLocalSearch(
                file_path=self.file_path, max_iterations=self.internal_iterations
                ).run(initial_solution=copy.deepcopy(self.current_routes))
            
            self.current_routes = local_search['routes']
            self.current_routes_cost = local_search['solution_cost']
            self.check_current_routes()
        
            if local_search['solution_cost'] == self.optimal_value:
                break
            
            self.max_iterations -= (self.internal_iterations - local_search['remaining_iterations'])

            if self.max_iterations < self.internal_iterations:
                self.internal_iterations = self.max_iterations

            

        return {
            'routes':self.best_routes,
            'solution_cost': round(self.best_cost, 2),
            'optimal_cost': self.optimal_value,
            'remaining_iterations': self.max_iterations
        }

simple_local_search = GRASPLocalSearch(max_iterations=1000, k_percentage=15, internal_iterations=100)
print(simple_local_search.run())
