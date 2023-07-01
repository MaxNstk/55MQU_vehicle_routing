import numpy as np

from utils import calculate_route_cost, get_distance_matrix, load_vrp_instance
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
            routes = [[1] for _ in range(self.num_vehicles)]
            # inicializa a lista de clientes disponiveis, a partir do 2 ate o ultimo
            available_customers = list(range(2, len(self.demands)+1))
            visited_customers = []

            current_route = routes[0]
            while available_customers:        
                max_iterations -= 1


                # seleciona os k melhores elementos a serem sorteados
                self.set_k_parameter(len(available_customers)-1)

                # seleciona os mais próximos baseados parametro k
                candidate_customers = self.get_k_based_customers(current_route[-1], available_customers)

                # sorteia um deles
                next_customer = self.get_next_customer(candidate_customers, self.get_remaining_capacity(current_route))

                # caso não haja proximo cliente disponivel para rota, erscolhemos outra aleatoriamente para utilizar
                if not next_customer:
                    current_route = routes[random.randint(0, (self.num_vehicles)-1)]
                    continue

                # adiciona o cliente na rota atual
                current_route.append(next_customer)
                available_customers.remove(next_customer)
                visited_customers.append(next_customer)

                # seleciona a rota baseado naquela que contem o menor numero de clientes
                current_route = min(routes, key=len)           
            
            for route in routes:
                route.append(1) 
            routes_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in routes)

            if not self.best_routes or routes_cost < self.best_cost:
                self.best_routes, self.best_cost = routes, routes_cost 

            if self.best_cost == self.optimal_value:
                break
            
        return self.best_routes, self.best_cost, self.optimal_value

semi_greedy = SemiGreedyCRVP(file_path="instances\A\A-n32-k5.vrp")
print(semi_greedy.run(max_iterations=5000, k_percentage=50))