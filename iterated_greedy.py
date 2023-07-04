from semi_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem
import random


# TODO impedir a remoção da primeira e ultima rota, verificar 
# por que clientes disponíveis ja estão em rotas
class IteratedGreedyCRVP(VehicleRoutingProblem):

    """ Construtiva semi gulosa, preenche um caminhão de cada vez, 
    melhorar para verificar em qual caminhão deve ser posto """        
    
    def destroy_solution(self):
        self.available_customers = []
        self.visited_customers = self.get_all_customers()

        # remove elementos aleatórios das rotas, dado o parametro D
        customers_to_destoy = random.sample(self.visited_customers, self.D)
        for customer in customers_to_destoy:
            self.available_customers.append(customer)
            self.visited_customers.remove(customer)
        
        # monta as novas rotas, removendo os elementos selecionados acima
        for idx, route in enumerate(self.current_routes):
            new_route = route
            del new_route[-1]
            new_route = [customer for customer in route if customer not in self.available_customers]
            self.current_routes[idx] = new_route

    def set_desctruction_amount(self, destruction_percentage):
        self.D = int((len(self.demands)-1) * (destruction_percentage / 100))
        self.D = 1 if not self.D else self.D
    
    def check_current_routes(self):
        self.current_routes_cost = self.get_routes_cost(self.current_routes)
        if self.current_routes_cost < self.best_cost:
            self.best_routes, self.best_cost = self.current_routes, self.current_routes_cost

    def run(self, max_iterations, destruction_percentage, k_percentage):
        self.max_iterations = max_iterations

        # define a quantidade de elementos a serem destruidos da solução atual
        self.set_desctruction_amount(destruction_percentage)
        
        # cria uma instancia do semi_greedy para usar para solução inicial e reconstrução das rotas
        semi_greedy =  SemiGreedyCRVP(k_percentage=k_percentage, file_path=self.file_path)

        #define solução inicial
        initial_solution = semi_greedy.run()

        self.best_routes, self.best_cost = initial_solution['routes'], initial_solution['solution_cost']

        while self.max_iterations > 0:

            # atribui a solução atual a melhor encontrada ate então
            self.current_routes, self.current_routes_cost = self.best_routes, self.best_cost

            #destroi parcialmente a solução
            self.destroy_solution()

            #reconstroi a solução com o semi guloso
            self.available_customers, self.current_routes = semi_greedy.get_semi_greedy_routes(self.available_customers, self.current_routes)

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
            'optimal_cost': self.optimal_value
        }

semi_greedy = IteratedGreedyCRVP()
print(semi_greedy.run(max_iterations=5000, destruction_percentage=20, k_percentage=20))