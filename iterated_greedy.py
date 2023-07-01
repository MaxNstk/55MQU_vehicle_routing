import numpy as np
from construtiva_semi_gulosa import SemiGreedyCRVP

from utils import calculate_route_cost, get_distance_matrix, load_vrp_instance
from vehicle_routing_problem import VehicleRoutingProblem


class IteratedGreedyCRVP(VehicleRoutingProblem):
    
    def get_sorted_customers(self, available_customers, current_customer):
        candidate_customers = []
        for customer in available_customers:
            distance = self.dist_matrix[current_customer][customer]
            candidate_customers.append((customer, distance))
        candidate_customers.sort(key=lambda x: x[1])
        return list(map(lambda x: x[0], candidate_customers))
    
    def get_next_customer(self, customers, capacity):
        next_customer = None
        for _ in customers:
            chosen_customer = np.random.choice(customers)
            if self.demands[chosen_customer] <= capacity:
                return chosen_customer     
            customers.remove(chosen_customer)
        return next_customer
    
    def destroy_solution(self, solution):
        # Remove randomly selected customers from the routes
        for i in range(len(solution)):
            route = solution[i]
            if len(route) > 2:
                remove_customer = np.random.choice(route[1:-1])
                route.remove(remove_customer)
        return solution
    
    def reconstruct_solution(self, solution):
        # Insert randomly selected customers back into the routes
        available_customers = list(range(1, self.dimension + 1))
        for route in solution:
            available_customers.remove(route[0])
            available_customers.remove(route[-1])
        
        for i in range(len(solution)):
            route = solution[i]
            remaining_capacity = self.vehicle_capacity - sum(self.demands[customer] for customer in route)
            while remaining_capacity > 0 and available_customers:
                next_customer = self.get_next_customer(available_customers, remaining_capacity)
                if next_customer is not None:
                    route.append(next_customer)
                    available_customers.remove(next_customer)
                    remaining_capacity -= self.demands[next_customer]
                else:
                    break
        return solution
    
    def run(self, max_iterations, destroy_percentage, reconstruct_percentage):
        best_routes = None
        best_cost = None
        
        num_customers = len(self.demands) - 1

        for iteration in range(max_iterations):
            # Construct initial solution using a semi-greedy approach
            semi_greedy = SemiGreedyCRVP(self.file_path)
            solution = semi_greedy.run(1, 0)
            
            # Improve the solution using the Iterated Greedy approach
            for _ in range(destroy_percentage):
                destroyed_solution = self.destroy_solution(solution)
                reconstructed_solution = self.reconstruct_solution(destroyed_solution)
                
                # Calculate the cost of the reconstructed solution
                total_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in reconstructed_solution)
                
                # Update the best solution if the cost is lower
                if best_cost is None or total_cost < best_cost:
                    best_cost = total_cost
                    best_routes = reconstructed_solution
            
            # Check if the optimal value has been reached
            if best_cost == self.optimal_value:
                return best_routes
            
        return best_routes, best_cost, self.optimal_value
