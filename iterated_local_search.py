import random
import copy
from semi_greedy import SemiGreedyCRVP
from simple_local_search import SimpleLocalSearch
from vehicle_routing_problem import VehicleRoutingProblem

class IteratedLocalSearch(VehicleRoutingProblem):

    def __init__(self,max_iterations, k_percentage, n_distortion,  file_path="instances\A\A-n32-k5.vrp"):
        super().__init__(file_path)
        self.max_iterations = max_iterations
        self.n_distortion = n_distortion
        self.semi_greedy = SemiGreedyCRVP(k_percentage=k_percentage, file_path=self.file_path)

    def change_customers_route(self):
        
        # seleciona duas rotas aleatorias
        first_route = self.get_random_route()
        second_route = self.get_random_route()

        # seleciona dois clientes aleatorios das rotas, excluindo o deposito
        first_customer = random.choice(first_route[1:-1])
        first_customer_idx = first_route.index(first_customer)

        second_customer = first_customer
        while second_customer == first_customer:
            second_customer = random.choice(second_route[1:-1])
        second_customer_idx = second_route.index(second_customer)

        # troca as os clientes nas rotas escolhidas
        first_route[first_customer_idx] = second_customer
        second_route[second_customer_idx] = first_customer

    # Função que implementa o algoritmo de busca local iterada
    def run(self):
        #define solução inicial
        initial_solution = self.semi_greedy.run()

        self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']

        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while self.max_iterations > 0:

            local_search = SimpleLocalSearch(
                file_path=self.file_path, max_iterations=self.max_iterations
                ).run(initial_solution=copy.deepcopy(self.current_routes))
            
            if local_search['solution_cost'] == self.optimal_value:
                break
            self.max_iterations = local_search['remaining_iterations']
            self.current_routes = local_search['routes']
            self.current_routes_cost = self.get_routes_cost(self.current_routes)
 
            for _ in range(self.n_distortion):
                self.change_customers_route()

        return {
            'routes':self.current_routes,
            'solution_cost': round(self.current_routes_cost, 2),
            'optimal_cost': self.optimal_value,
            'max_iterations': self.max_iterations
        }

simple_local_search = IteratedLocalSearch(max_iterations=1000, k_percentage=15, n_distortion=2)
print(simple_local_search.run())
