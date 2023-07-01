from construtiva_semi_gulosa import SemiGreedyCRVP
from vehicle_routing_problem import VehicleRoutingProblem
from utils import calculate_route_cost, load_vrp_instance

class SimpleLocalSearch(VehicleRoutingProblem):

    # Função que implementa o algoritmo de busca local simples
    def run(self, max_iterations, k_percentage):

        # Calcular o valor de k baseado no percentual fornecido
        num_customers = len(self.demands) - 1
        self.k = int(num_customers * (k_percentage / 100))

        # Gera a solução inicial utilizando o SemiGreedy
        semi_greedy = SemiGreedyCRVP()

        initial_solution = semi_greedy.run(10, 15)[0]
        current_solution = initial_solution

        # Verifica custo de solução e atribui como o melhor até o momento
        self.best_routes = current_solution
        self.best_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in self.best_routes)

        iteration = 0

        # Critério de parada: Máximo de iterações e encontro da solução ótima
        while iteration < max_iterations:
            
            # Incrementa o contador
            iteration += 1

            # Percorra todas as rotas possíveis para encontrar a melhor vizinhança
            for i in range(len(current_solution)):
                for j in range(len(current_solution[i])):

                    # Realize a troca de clientes entre as rotas
                    customer1 = current_solution[i][j]
                    customer2 = current_solution[j][i]
                    current_solution[i][j] = customer2
                    current_solution[j][i] = customer1

                    # Avalie o custo da nova solução
                    neighbor_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in current_solution)

                    # Verifique se é a melhor vizinhança encontrada
                    if neighbor_cost < self.best_cost:
                        best_neighbor = current_solution
                        self.best_cost = neighbor_cost

                    # Desfaça a troca para a próxima iteração
                    current_solution[i][j] = customer1
                    current_solution[j][i] = customer2

            # Atribuindo solução gerada à atual
            best_solution = best_neighbor

            # Verifica o custo da solução
            neighbor_cost = sum(calculate_route_cost(route, self.dist_matrix) for route in best_solution)

            # Verifica se a solução gerada é melhor
            if neighbor_cost < self.best_cost:
                self.best_routes = best_solution
                self.best_cost = neighbor_cost

            # Verifica se solução gerada é a ideal
            if self.best_cost == self.optimal_value:
                return self.best_routes, self.best_cost

        return self.best_routes, self.best_cost