import numpy as np

from vehicle_routing_problem import VehicleRoutingProblem
import random


# TODO garantir que todos caminhoes sejam usados. preencher todos caminhoões simultaneamente ou com alguma outra estratégia

class SemiGreedyCRVP(VehicleRoutingProblem):

    """ Construtiva semi gulosa, preenche um caminhão de cada vez, 
    melhorar para verificar em qual caminhão deve ser posto """

    k_percentage = None
    k = None

    def get_k_based_customers(self, current_customer, available_customers):
        return self.get_closest_customers(current_customer,available_customers)[:self.k]
    
    def get_next_customer(self, customers, capacity):
        next_customer = None
        for _ in customers:
            chosen_customer = np.random.choice(customers)
            if self.demands[chosen_customer] <= capacity:
                return chosen_customer     
            customers.remove(chosen_customer)
        return next_customer
    
    def set_k_parameter(self,customers_amount):
        self.k = int(customers_amount * (self.k_percentage / 100))
        self.k = 1 if not self.k else self.k

    def run(self, max_iterations, k_percentage):
        self.k_percentage = k_percentage

        # armazena o melhor conjunto de rotas e custos 
        self.best_routes = []
        self.best_cost = None       

        # acha boas soluções de forma semi-aleatória até o limite de iterações
        for iteration in range(max_iterations):

            # Inicializar as rotas 
            self.current_routes = [[1] for _ in range(self.num_vehicles)]
            # inicializa a lista de clientes disponiveis, a partir do 2 ate o ultimo
            self.available_customers = list(range(2, len(self.demands)+1))
            visited_customers = []

            current_route = self.current_routes[0]
            while self.available_customers:        
                max_iterations -= 1


                # seleciona os k melhores elementos a serem sorteados
                self.set_k_parameter(len(self.available_customers)-1)

                # seleciona os mais próximos baseados parametro k
                candidate_customers = self.get_k_based_customers(current_route[-1], self.available_customers)

                # sorteia um deles
                next_customer = self.get_next_customer(candidate_customers, self.get_remaining_capacity(current_route))

                # caso não haja proximo cliente disponivel para rota, erscolhemos outra aleatoriamente para utilizar
                if not next_customer:
                    break

                # adiciona o cliente na rota atual
                current_route.append(next_customer)
                self.available_customers.remove(next_customer)
                visited_customers.append(next_customer)

                # seleciona a rota baseado naquela que contem o menor numero de clientes
                current_route = self.get_route_with_more_capacity(self.current_routes)          
            
            if self.available_customers:
                continue

            for route in self.current_routes:
                route.append(1) 
            self.routes_cost = self.calculate_solution_cost(self.current_routes)

            if not self.best_routes or self.routes_cost < self.best_cost:
                self.best_routes, self.best_cost = self.current_routes, self.routes_cost 

            if self.best_cost == self.optimal_value:
                break
            
        return self.best_routes, self.best_cost, self.optimal_value

semi_greedy = SemiGreedyCRVP()
print(semi_greedy.run(max_iterations=1000, k_percentage=50))