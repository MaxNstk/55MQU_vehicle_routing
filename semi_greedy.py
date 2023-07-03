import numpy as np

from vehicle_routing_problem import VehicleRoutingProblem
import random



class SemiGreedyCRVP(VehicleRoutingProblem):

    """ Construtiva semi gulosa,  """

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
    
    def set_k_customers_amount(self,customers_amount):
        self.k = int(customers_amount * (self.k_percentage / 100))
        self.k = 1 if not self.k else self.k
    
    def get_semi_greedy_routes(self):

        while self.available_customers:

            # seleciona a rota baseado naquela que tem a maior capacidade disponível
            current_route = self.get_route_with_more_capacity(self.current_routes)

            # define a quantidade k de elementos baseados no parâmetro recebido
            self.set_k_customers_amount(len(self.available_customers)-1)

            # seleciona os mais próximos e corta a lista em k elementos
            candidate_customers = self.get_k_based_customers(current_route[-1], self.available_customers)

            # sorteia um deles aleatóriamente, caso tenha espaço na rota adiciona, se não seleciona outra
            next_customer = self.get_next_customer(candidate_customers, self.get_remaining_capacity(current_route))

            # caso não haja proximo cliente disponivel para rota, encerramos ela
            if not next_customer:
                break

            # adiciona o cliente na rota atual
            current_route.append(next_customer)
            self.available_customers.remove(next_customer)

    def run(self, k_percentage):
        self.k_percentage = k_percentage

        self.initialize_customers()
        while self.available_customers:
            self.initialize_empty_routes()
            self.initialize_customers()
            self.get_semi_greedy_routes()

        self.add_deposit_to_routes(self.current_routes) 

        return {
            'routes':self.current_routes,
            'solution_cost': round(self.get_routes_cost(self.current_routes), 2),
            'optimal_cost': self.optimal_value
        }

# semi_greedy = SemiGreedyCRVP()
# print(semi_greedy.run(k_percentage=50))