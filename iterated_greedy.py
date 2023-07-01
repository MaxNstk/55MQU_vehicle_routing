import numpy as np
from utils import calculate_route_cost
from vehicle_routing_problem import VehicleRoutingProblem

class IteratedGreedyCRVP(VehicleRoutingProblem):

    k = 0.5
    
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
        best_routes = []
        best_cost = None
        
        # Calcular o valor de k baseado no percentual fornecido
        num_customers = len(self.demands) - 1
        self.k = int(num_customers * (k_percentage / 100))

        # Acha boas soluções de forma semi-aleatória até o limite de iterações
        for iteration in range(max_iterations):
            routes = [[1] for _ in range(self.num_vehicles)]
            available_customers = list(range(1, num_customers + 1))
            visited_customers = []
            
            # Construir as rotas usando a estratégia semi-gulosa
            while available_customers:
                # Selecionar o próximo caminhão disponível
                current_vehicle = len(routes) % self.num_vehicles
                
                # Selecionar o próximo cliente baseado na estratégia semi-gulosa
                current_route = routes[current_vehicle]
                current_customer = current_route[-1]
                remaining_capacity = self.vehicle_capacity - sum(self.demands[route] for route in current_route)
                candidate_customers = self.get_sorted_customers(available_customers, current_customer)
                next_customer = self.get_next_customer(candidate_customers, remaining_capacity)
                
                # Se nenhum cliente puder ser alocado, finalizar a rota atual do caminhão
                if next_customer is None:
                    current_route.append(1)
                else:
                    current_route.append(next_customer)
                    available_customers.remove(next_customer)
                    visited_customers.append(next_customer)
            
            # Calcular o custo total das rotas
            total_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in routes)
            
            # Verificar o custo das rotas
            if not best_cost or total_cost < best_cost:
                best_cost = total_cost
                best_routes = routes
            
            if best_cost == self.optimal_value:
                return best_routes
            
        return best_routes, best_cost, self.optimal_value
