import random
from iterated_greedy import IteratedGreedyCRVP
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
        iterated_greedy = IteratedGreedyCRVP()

        initial_solution = iterated_greedy.run(max_iterations=1, destruction_percentage=20)
        self.best_routes, self.best_cost = initial_solution[0], initial_solution[1]

        iteration = 0

        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while iteration < max_iterations:
            
            # Incrementa o contador
            iteration += 1

            self.current_routes, self.current_routes_cost = self.best_routes, self.best_cost
            self.change_customers_route()

            self.current_routes_cost = self.calculate_solution_cost(self.current_routes)

            if self.current_routes_cost < self.best_cost:
               self.best_routes, self.best_cost = self.current_routes, self.current_routes_cost

            # Verifica se solução gerada é a ideal
            if self.best_cost == self.optimal_value:
                return self.best_routes, self.best_cost

        return self.best_routes, self.best_cost
    

simple_local_search = SimpleLocalSearch()
print(simple_local_search.run(5000))