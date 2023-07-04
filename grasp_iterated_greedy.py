from iterated_greedy import IteratedGreedyCRVP
from semi_greedy import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem
import random


# TODO impedir a remoção da primeira e ultima rota, verificar 
# por que clientes disponíveis ja estão em rotas
class GRASPIteratedGreedyCRVP(IteratedGreedyCRVP):

    """ Construtiva semi gulosa, preenche um caminhão de cada vez, 
    melhorar para verificar em qual caminhão deve ser posto """        

    def __init__(self, max_iterations, destruction_percentage, k_percentage, internal_iterations, file_path="instances\A\A-n32-k5.vrp"):
        self.internal_iterations = internal_iterations
        super().__init__(max_iterations, destruction_percentage, k_percentage, file_path)
    

    def run(self):     
        while self.max_iterations > 0:
   
            initial_solution = self.semi_greedy.run()
            self.current_routes, self.current_routes_cost = initial_solution['routes'], initial_solution['solution_cost']
            self.check_current_routes()

            internal_iterations = self.internal_iterations
            while internal_iterations > 0:
                internal_iterations -=1
                self.max_iterations -=1

                # atribui a solução atual a melhor encontrada ate então
                self.current_routes, self.current_routes_cost = self.best_routes, self.best_cost

                #destroi parcialmente a solução
                self.destroy_solution()

                #reconstroi a solução com o semi guloso
                self.available_customers, self.current_routes = self.semi_greedy.get_semi_greedy_routes(self.available_customers, self.current_routes)

                # verifica se faltou visitar alguem e continua, a rota é invalidada
                if self.available_customers:
                    continue

                self.add_deposit_to_routes(self.current_routes)
                # faz a verificação se houve melhora
                self.check_current_routes()

                if self.best_cost == self.optimal_value:
                    break
                     
        return {
            'routes':self.best_routes,
            'solution_cost': round(self.best_cost, 2),
            'optimal_cost': self.optimal_value
        }

iterated_greedy = GRASPIteratedGreedyCRVP(max_iterations=5000, destruction_percentage=20, k_percentage=20, internal_iterations=100)
print(iterated_greedy.run())