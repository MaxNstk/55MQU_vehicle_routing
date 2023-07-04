import numpy as np

from vehicle_routing_problem import VehicleRoutingProblem
import random



class SemiGreedyCRVP(VehicleRoutingProblem):

    """ Construtiva semi gulosa,  """

    k_percentage = None
    k = None

    def __init__(self,k_percentage, file_path="instances\A\A-n32-k5.vrp"):
        self.k_percentage = k_percentage
        super().__init__(file_path)

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
    
    def get_semi_greedy_routes(self, available_customers, current_routes):

        while available_customers:

            # seleciona a rota baseado naquela que tem a maior capacidade disponível
            current_route = self.get_route_with_more_capacity(current_routes)

            # define a quantidade k de elementos baseados no parâmetro recebido
            self.set_k_customers_amount(len(available_customers)-1)

            # seleciona os mais próximos e corta a lista em k elementos
            candidate_customers = self.get_k_based_customers(current_route[-1], available_customers)

            # sorteia um deles aleatóriamente, caso tenha espaço na rota adiciona, se não seleciona outra
            next_customer = self.get_next_customer(candidate_customers, self.get_remaining_capacity(current_route))

            # caso não haja proximo cliente disponivel para rota, encerramos ela
            if not next_customer:
                break

            # adiciona o cliente na rota atual
            current_route.append(next_customer)
            available_customers.remove(next_customer)
        return available_customers, current_routes

    def run(self):

        self.get_all_customers()
        self.available_customers = True
        while self.available_customers:
            self.current_routes = self.get_empty_routes()
            self.available_customers = self.get_all_customers()
            self.available_customers, self.current_routes = self.get_semi_greedy_routes(self.available_customers, self.current_routes)

        self.add_deposit_to_routes(self.current_routes) 

        return {
            'routes':self.current_routes,
            'solution_cost': round(self.get_routes_cost(self.current_routes), 2),
            'optimal_cost': self.optimal_value
        }

# semi_greedy = SemiGreedyCRVP(k_percentage=50)
# print(semi_greedy.run())