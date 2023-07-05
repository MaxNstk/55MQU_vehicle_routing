import random
import copy
from semi_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem

class SimpleLocalSearch(VehicleRoutingProblem):

    def __init__(self,max_iterations, file_path="instances\A\A-n32-k5.vrp"):
        self.max_iterations = max_iterations
        super().__init__(file_path)
    
    def change_intra_route_customers(self, route):
        first_customer = random.choice(route[1:-1])
        first_customer_idx = route.index(first_customer)

        second_customer = first_customer
        while first_customer == second_customer:
            second_customer = random.choice(route[1:-1])

        second_customer_idx = route.index(second_customer)
        route[first_customer_idx] = second_customer
        route[second_customer_idx] = first_customer
        return route
    
    def change_inter_routes_customers(self, route1, route2):
        first_customer = random.choice(route1[1:-1])
        first_customer_idx = route1.index(first_customer)

        second_customer = random.choice(route2[1:-1])
        second_customer_idx = route2.index(second_customer)
        
        route1[first_customer_idx] = second_customer
        route2[second_customer_idx] = first_customer
        return route1, route2

    
    # def get_better_routes_old(self):
    #     self.better_routes = []
    #     self.alternative_solutions = []
    #     for idx in range(len(self.current_routes)-1):

    #         # faz uma troca entre clientes na rota aual
    #         base_routes = copy.deepcopy(self.current_routes)
    #         base_routes[idx] = self.change_intra_route_customers(base_routes[idx])
    #         if self.get_routes_cost(base_routes) < self.current_routes_cost:
    #             self.better_routes.append(base_routes)
    #         else:
    #             self.alternative_solutions.append(base_routes)
    #         self.max_iterations -= 1

    #         # troca um cliente aleatório entre as próximas rotas
    #         for i in range(idx,len(self.current_routes)-2):
    #             base_routes = copy.deepcopy(self.current_routes)
    #             base_routes[idx], base_routes[i+1] = self.change_inter_routes_customers(base_routes[idx], base_routes[i+1])
    #             if self.get_routes_cost(base_routes) < self.current_routes_cost:
    #                 self.better_routes.append(base_routes)
    #             else:
    #                 self.alternative_solutions.append(base_routes)
    #             self.max_iterations -= 1
    
        
    # def get_better_routes(self):
    #     self.better_routes = []
    #     self.alternative_solutions = []

    #     # para cada uma das rotas
    #     for route_idx in range(len(self.current_routes)-1):

    #         # para cada cliente dessa rota
    #         for customer_idx in range(len(self.current_routes[route_idx])-2):
                
    #             base_customer = base_routes[customer_idx]
    #             # faz a troca com todos demais clientes da rota
    #             for idx in range(customer_idx+1, len(self.current_routes[route_idx])-2):
    #                 base_routes = copy.deepcopy(self.current_routes)

    #                 base_routes[customer_idx] = base_routes[idx]
    #                 base_routes[idx] = base_customer
                
    #         base_routes[idx] = self.change_intra_route_customers(base_routes[idx])
    #         if self.get_routes_cost(base_routes) < self.current_routes_cost:
    #             self.better_routes.append(base_routes)
    #         else:
    #             self.alternative_solutions.append(base_routes)
    #         self.max_iterations -= 1

    #         # troca um cliente aleatório entre as próximas rotas
    #         for i in range(idx,len(self.current_routes)-2):
    #             base_routes = copy.deepcopy(self.current_routes)
    #             base_routes[idx], base_routes[i+1] = self.change_inter_routes_customers(base_routes[idx], base_routes[i+1])
    #             if self.get_routes_cost(base_routes) < self.current_routes_cost:
    #                 self.better_routes.append(base_routes)
    #             else:
    #                 self.alternative_solutions.append(base_routes)
    #             self.max_iterations -= 1

    def get_better_neighbors(self, current_routes):
        neighbors = []

        # Percorre todas as rotas
        for route_index, route in enumerate(current_routes):

            # Percorre todos os elementos da rota, excluindo o depósito
            for i in range(1, len(route) - 1):

                # Troca o elemento atual com todos os elementos da mesma rota
                for j in range(1, len(route) - 1):

                    # Cria uma cópia do conjunto de rotas
                    new_routes = copy.deepcopy(current_routes)

                    # Troca os elementos
                    new_routes[route_index][i], new_routes[route_index][j] = new_routes[route_index][j], new_routes[route_index][i]

                    # Adiciona as novas rotas à lista de vizinhos caso seja melhor
                    if self.get_routes_cost(new_routes) < self.current_routes_cost:
                        neighbors.append(new_routes)

                # Troca o elemento atual com todos os elementos das outras rotas
                for other_route_index in range(len(current_routes)):
                    if other_route_index != route_index:
                        for j in range(1, len(current_routes[other_route_index]) - 1):
                        
                            # Cria uma cópia do conjunto de rotas
                            new_routes = copy.deepcopy(current_routes)

                            # Troca os elementos
                            new_routes[route_index][i], new_routes[other_route_index][j] = new_routes[other_route_index][j], new_routes[route_index][i]

                            # Adiciona as novas rotas à lista de vizinhos
                            if self.get_routes_cost(new_routes) < self.current_routes_cost:
                                neighbors.append(new_routes)

        return neighbors

    # Função que implementa o algoritmo de busca local simples
    def run(self, initial_solution=None):

        #define solução inicial
        if not initial_solution:
            initial_solution = SemiGreedyCRVP(k_percentage=100, file_path=self.file_path).run()
            self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']
        else:
            self.current_routes, self.current_routes_cost = initial_solution, self.get_routes_cost(initial_solution)

        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while self.max_iterations > 0:

            # faz pequenas modificações e grava na lista de better routes aquelas que geraram algum            
            self.better_routes = self.get_better_neighbors(self.current_routes)

            # verifica se não há soluções com ganho
            if not self.better_routes:
                break

            self.current_routes = random.choice(self.better_routes)
            self.current_routes_cost = self.get_routes_cost(self.current_routes)

            # Verifica se solução gerada é a ideal
            if self.current_routes_cost == self.optimal_value:
                break

            self.max_iterations -= 1

        return {
            'routes':self.current_routes,
            'solution_cost': round(self.current_routes_cost, 2),
            'optimal_cost': self.optimal_value,
            'remaining_iterations': self.max_iterations,
        }

# simple_local_search = SimpleLocalSearch(1000)
# print(simple_local_search.run())
