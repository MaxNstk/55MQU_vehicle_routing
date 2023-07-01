import numpy as np

from utils import calculate_route_cost, get_distance_matrix, load_vrp_instance
from vehicle_routing_problem import VehicleRoutingProblem


class SemiGreedyCRVP(VehicleRoutingProblem):
    """ Construtiva semi gulosa, preenche um caminhão de cada vez, 
    melhorar para verificar em qual caminhão deve ser posto """
    
    k = 0.5

    def __init__(self, file_path="instances\A\A-n32-k5.vrp") -> None:
        self.file_path = file_path

        self.vehicle_capacity, self.num_vehicles, self.optimal_value, self.dimension, self.node_coords, self.demands = load_vrp_instance(file_path)
        self.dist_matrix = get_distance_matrix(self.dimension, self.node_coords)
    
    def get_sorted_customers(self, available_customers, current_customer):
        candidate_customers = []
        for customer in available_customers:
            distance = self.dist_matrix[current_customer][customer]
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

        # armzaze o melhor conjunto de rotas até então
        self.best_routes = []
        self.best_cost = None
        
        # Calcular o valor de k baseado no percentual fornecido
        num_customers = len(self.demands) - 1
        self.k = int(num_customers * (k_percentage / 100))

        # acha boas soluções de forma semi-aleatória até o limite de iterações
        for iteration in range(max_iterations):

            # Inicializar as rotas e as listas de clientes disponíveis e visitados
            routes = [[1] for _ in range(self.num_vehicles)]
            available_customers = list(range(1, num_customers + 1))
            visited_customers = []
            
            # Criar uma rota inicial cpm a saida no primerio nó (deposito)
            sorted_customers = self.get_sorted_customers(available_customers,1)
            initial_customer = np.random.choice(sorted_customers)
            current_route = [1, initial_customer]
            available_customers.remove(initial_customer)
            visited_customers.append(initial_customer)
            
            # Construir as rotas usando a estratégia semi-gulosa
            while available_customers:
                max_iterations -= 1
                # pega o cliente atual e a capacidade disponível
                current_customer = current_route[-1]
                remaining_capacity = self.vehicle_capacity - sum(self.demands[route] for route in current_route)
                
                # Selecionar os k clientes mais próximos disponíveis
                candidate_customers = self.get_sorted_customers(available_customers, current_customer)
                
                # Selecionar o próximo cliente baseado na demanda e na capacidade restante
                next_customer = self.get_next_customer(candidate_customers, remaining_capacity)
                
                # Se nenhum cliente puder ser alocado, finalizar a rota atual
                if next_customer is None:
                    current_route.append(1)
                    routes.append(current_route)
                    current_route = [1]
                else:
                    current_route.append(next_customer)
                    available_customers.remove(next_customer)
                    visited_customers.append(next_customer)
            
            # Adicionar a última rota gerada
            if iteration < self.num_vehicles:
                self.best_routes = routes
            
            # Calcular o custo total das rotas
            total_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in routes)

            # verificar o custo das rotas
            if not self.best_cost:
                self.best_cost = total_cost
            self.best_cost = total_cost if total_cost < self.best_cost else self.best_cost

            if self.best_cost == self.optimal_value:
                return routes
            
        return self.best_routes, self.best_cost, self.optimal_value