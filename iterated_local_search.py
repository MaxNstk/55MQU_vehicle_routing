import random
from iterated_greedy import IteratedGreedyCRVP
from semy_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem

class IteratedLocalSearch(VehicleRoutingProblem):

    def complete_missing_routes(self):
        while self.available_customers:
            current_route = self.get_route_with_more_capacity(self.current_routes)
            chosen_customer = self.get_closest_customers(current_route[-1], self.available_customers)[0]
            current_route.append(chosen_customer)
            self.available_customers.remove(chosen_customer)
        for route in self.current_routes:
            if route[-1] != 1:
                route.append(1)
    
    def detroy_routes(self):
        routes_to_destroy = random.sample(range(len(self.current_routes)-1),self.destruction_number)
        self.available_customers = []
        for i in range(self.destruction_number):
            self.available_customers.extend(self.current_routes[routes_to_destroy[i]][1:-1])
            self.current_routes[routes_to_destroy[i]] = [1]

    # Função que implementa o algoritmo de busca local iterada
    def run(self, max_iterations, destruction_number): 
        self.destruction_number = destruction_number

        # Gera a solução inicial utilizando o SemiGreedy
        semi_greedy = SemiGreedyCRVP(self.file_path)

        initial_solution = semi_greedy.run(max_iterations=1, k_percentage=20)

        while not initial_solution[0]:
            initial_solution = semi_greedy.run(max_iterations=1, k_percentage=20)
        self.best_routes, self.best_cost = initial_solution[0], initial_solution[1]

        iteration = 0

        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while iteration < max_iterations:
            
            # Incrementa o contador
            iteration += 1
            self.current_routes, self.current_routes_cost = self.best_routes, self.best_cost

            self.detroy_routes()
            self.complete_missing_routes()

            self.current_routes_cost = self.calculate_solution_cost(self.current_routes)

            if self.current_routes_cost < self.best_cost:
               self.best_routes, self.best_cost = self.current_routes, self.current_routes_cost

            # Verifica se solução gerada é a ideal
            if self.best_cost == self.optimal_value:
                return self.best_routes, self.best_cost

        return self.best_routes, self.best_cost, self.optimal_value
    

simple_local_search = IteratedLocalSearch('instances/A/A-n80-k10.vrp')
print(simple_local_search.run(5000, 2))