from semi_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem
import random

class IteratedGreedyCRVP(VehicleRoutingProblem):
   

    def __init__(self,max_iterations, destruction_percentage, k_percentage, file_path="instances\A\A-n32-k5.vrp"):
        super().__init__(file_path)
        self.max_iterations = max_iterations

        # define a quantidade de elementos a serem destruidos da solução atual
        self.set_desctruction_amount(destruction_percentage)
        
        # cria uma instancia do semi_greedy para usar para solução inicial e reconstrução das rotas
        self.semi_greedy = SemiGreedyCRVP(k_percentage=k_percentage, file_path=self.file_path)
        
    
    def destroy_solution(self):
        # remove elementos aleatórios das rotas, dado o parametro D
        customers_to_destoy = random.sample(self.get_all_customers(), self.D)

        # monta as novas rotas, removendo os elementos selecionados acima
        for idx, route in enumerate(self.current_routes):
            new_route = route
            del new_route[-1]
            new_route = [customer for customer in route if customer not in customers_to_destoy]
            self.current_routes[idx] = new_route
    
    def get_available_customers(self):
        self.available_customers = self.get_all_customers()
        for route in self.current_routes:
            for customer in route:
                if customer in self.available_customers:
                    self.available_customers.remove(customer)

    def run(self, initial_solution=None):

        #define solução inicial
        if not initial_solution:
            initial_solution = SemiGreedyCRVP(k_percentage=100, file_path=self.file_path).run()
            self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']
        else:
            self.current_routes, self.current_routes_cost = initial_solution, self.get_routes_cost(initial_solution)

        while self.max_iterations > 0:
        
            #destroi parcialmente a solução
            self.destroy_solution()
            self.get_available_customers()
            #reconstroi a solução com o semi guloso
            self.available_customers, self.current_routes = self.semi_greedy.get_semi_greedy_routes(self.available_customers, self.current_routes)

            # verifica se faltou visitar alguem e continua, a rota é invalidada
            if self.available_customers:
                continue

            self.add_deposit_to_routes(self.current_routes)
            # faz a verificação se houve melhora
            self.check_current_routes()

            self.max_iterations -= 1
            if self.best_cost == self.optimal_value:
                break
                     
        return {
            'routes':self.best_routes,
            'solution_cost': round(self.best_cost, 2),
            'optimal_cost': self.optimal_value,
            'remaining_iterations': self.max_iterations
        }

# iterated_greedy = IteratedGreedyCRVP(max_iterations=5000, destruction_percentage=70, k_percentage=15, file_path="instances/A/A-n33-k6.vrp")
# print(iterated_greedy.run())