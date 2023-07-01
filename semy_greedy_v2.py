import numpy as np

from utils import calculate_route_cost, get_distance_matrix, load_vrp_instance
from vehicle_routing_problem import VehicleRoutingProblem


# TODO garantir que todos caminhoes sejam usados. preencher todos caminhoões simultaneamente ou com alguma outra estratégia

class SemiGreedyCRVP2(VehicleRoutingProblem):

    """ Construtiva semi gulosa, preenche um caminhão de cada vez, 
    melhorar para verificar em qual caminhão deve ser posto """
    k = None

    def get_sorted_customers(self, available_customers, current_customer):
        candidate_customers = []
        for customer in available_customers:
            distance = self.dist_matrix[current_customer-1][customer-1]
            candidate_customers.append((customer, distance))
        candidate_customers.sort(key=lambda x: x[1])
        candidate_customers = candidate_customers[:self.k]
        return list(map(lambda x: x[0], candidate_customers))
    
    def get_next_customer(self, customers, capacity):
        next_customer = None
        for _ in customers:
            chosen_customer = np.random.choice(customers)
            if self.demands[chosen_customer] <= capacity:
                return chosen_customer     
            customers.remove(chosen_customer)
        return next_customer
    

    def run(self, max_iterations, k_percentage):

        # armazena o melhor conjunto de rotas e melhores custos até então
        self.best_routes = []
        self.best_cost = None       

        # acha boas soluções de forma semi-aleatória até o limite de iterações
        for iteration in range(max_iterations):

            # Inicializar as rotas 
            routes = [[1] for _ in range(self.num_vehicles)]
            # inicializa a lista de clientes disponiveis, a partir do 2 ate o ultimo
            available_customers = list(range(2, len(self.demands)+1))
            visited_customers = []

            while available_customers:
               
                max_iterations -= 1

                # seleciona a rota baseado naquela que contem o menor numero de clientes
                current_route = min(routes, key=len)           

                # seleciona os k melhores elementos a serem sorteados
                customers_amount = len(available_customers)-1
                self.k = int(customers_amount * (k_percentage / 100))
                self.k = 1 if not self.k else self.k
                # seleciona os mais próximos baseados prametro k
                candidate_customers = self.get_sorted_customers(available_customers,current_route[-1])

                # sorteia um deles
                next_customer = self.get_next_customer(candidate_customers, self.vehicle_capacity)

                # adiciona o cliente na rota atual
                current_route.append(next_customer)
                available_customers.remove(next_customer)
                visited_customers.append(next_customer)
            
            for route in routes:
                route.append(1) 
            routes_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in routes)

            if not self.best_routes or routes_cost < self.best_cost:
                self.best_routes, self.best_cost = routes, routes_cost 

            if self.best_cost == self.optimal_value:
                break
            
        return self.best_routes, self.best_cost, self.optimal_value

semi_greedy = SemiGreedyCRVP2(file_path="instances\A\A-n32-k5.vrp")
print(semi_greedy.run(max_iterations=5000, k_percentage=50))