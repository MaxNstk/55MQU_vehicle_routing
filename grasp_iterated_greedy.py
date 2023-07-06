import copy
from iterated_greedy import IteratedGreedyCRVP
from semi_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem
import random


class GRASPIteratedGreedyCRVP(VehicleRoutingProblem):

    def __init__(self,max_iterations, destruction_percentage, k_percentage, internal_iterations, file_path="instances\A\A-n32-k5.vrp"):
        super().__init__(file_path)
        self.max_iterations = max_iterations
        self.internal_iterations = internal_iterations
        self.k_percentage = k_percentage
        # define a quantidade de elementos a serem destruidos da solução atual
        self.set_desctruction_amount(destruction_percentage)
        
        # cria uma instancia do semi_greedy para usar para solução inicial e reconstrução das rotas
        self.semi_greedy = SemiGreedyCRVP(k_percentage=k_percentage, file_path=self.file_path)


    def run(self, initial_solution=None):

        if not initial_solution:
            initial_solution = SemiGreedyCRVP(k_percentage=100, file_path=self.file_path).run()
            self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']
        else:
            self.current_routes, self.current_routes_cost = initial_solution, self.get_routes_cost(initial_solution)

        self.check_current_routes()

        while self.max_iterations > 0:

            #define solução inicial       
            initial_solution = self.semi_greedy.run()

            self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']

            iterated_greedy = IteratedGreedyCRVP(k_percentage=self.k_percentage,
                destruction_percentage=self.D,                                       
                file_path=self.file_path, max_iterations=self.internal_iterations,
                ).run(initial_solution=copy.deepcopy(self.current_routes))
            self.max_iterations -= self.internal_iterations
            
            self.current_routes, self.current_routes_cost = iterated_greedy['routes'], iterated_greedy['solution_cost']
            self.check_current_routes()

            if self.current_routes_cost == self.optimal_value:
                break

            if self.max_iterations < self.internal_iterations:
                self.internal_iterations = self.max_iterations

        return {
            'routes':self.best_routes,
            'solution_cost': round(self.best_cost, 2),
            'optimal_cost': self.optimal_value,
            'max_iterations': self.max_iterations
        }

# iterated_greedy = GRASPIteratedGreedyCRVP(max_iterations=5000, destruction_percentage=70, k_percentage=15,internal_iterations=1000, file_path="instances/A/A-n33-k6.vrp")
# print(iterated_greedy.run())