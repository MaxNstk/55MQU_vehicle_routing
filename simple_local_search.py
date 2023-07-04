import random
from semi_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem

class SimpleLocalSearch(VehicleRoutingProblem):

    def change_customers_route(self):
        
        # seleciona duas rotas aleatorias
        first_route = self.get_random_route()
        second_route = self.get_random_route()
        while first_route == second_route:
            second_route = self.get_random_route()

        # seleciona dois clientes aleatorios das rotas, excluindo o deposito
        first_customer = random.choice(first_route[1:-1])
        first_customer_idx = first_route.index(first_customer)

        second_customer = random.choice(second_route[1:-1])
        second_customer_idx = second_route.index(second_customer)

        # troca as os clientes nas rotas escolhidas
        first_route[first_customer_idx] = second_customer
        second_route[second_customer_idx] = first_customer


    # Função que implementa o algoritmo de busca local simples
    def run(self, max_iterations):

        # Gera a solução inicial utilizando o SemiGreedy
        semi_greedy = SemiGreedyCRVP(k_percentage=100, file_path=self.file_path)

        initial_solution = semi_greedy.run()

        self.best_routes, self.best_cost = initial_solution['routes'], initial_solution['solution_cost']

        iteration = 0

        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while iteration < max_iterations:
            
            # Incrementa o contador
            iteration += 1

            self.current_routes, self.current_routes_cost = self.best_routes, self.best_cost
            self.change_customers_route()

            self.current_routes_cost = self.get_routes_cost(self.current_routes)

            if self.current_routes_cost < self.best_cost:
               self.best_routes, self.best_cost = self.current_routes, self.current_routes_cost

            # Verifica se solução gerada é a ideal
            if self.best_cost == self.optimal_value:
                return self.best_routes, self.best_cost

        return self.best_routes, self.best_cost, self.optimal_value
    

# simple_local_search = SimpleLocalSearch()
# print(simple_local_search.run(5000))