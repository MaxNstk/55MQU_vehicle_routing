# import numpy as np
# from utils import get_distance_matrix, load_vrp_instance

# # Dados da instância
# # capacity = 100
# # num_vehicles = 5
# # optimal_value = 784
# # dimension = 32
# # node_coords = {
# #     1: (82, 76),
# #     2: (96, 44),
# #     3: (50, 5),
# #     4: (49, 8),
# #     5: (13, 7),
# #     6: (29, 89),
# #     7: (58, 30),
# #     8: (84, 39),
# #     9: (14, 24),
# #     10: (2, 39),
# #     11: (3, 82),
# #     12: (5, 10),
# #     13: (98, 52),
# #     14: (84, 25),
# #     15: (61, 59),
# #     16: (1, 65),
# #     17: (88, 51),
# #     18: (91, 2),
# #     19: (19, 32),
# #     20: (93, 3),
# #     21: (50, 93),
# #     22: (98, 14),
# #     23: (5, 42),
# #     24: (42, 9),
# #     25: (61, 62),
# #     26: (9, 97),
# #     27: (80, 55),
# #     28: (57, 69),
# #     29: (23, 15),
# #     30: (20, 70),
# #     31: (85, 60),
# #     32: (98, 5)
# # }
# # demands = {
# #     1: 0, 2: 19, 3: 21, 4: 6, 5: 19, 6: 7, 7: 12, 8: 16, 9: 6, 10: 16,
# #     11: 8, 12: 14, 13: 21, 14: 16, 15: 3, 16: 22, 17: 18, 18: 19, 19: 1,
# #     20: 24, 21: 8, 22: 12, 23: 4, 24: 8, 25: 24, 26: 24, 27: 2, 28: 20,
# #     29: 15, 30: 2, 31: 14, 32: 9
# # }
# capacity, num_vehicles, optimal_value, dimension, node_coords, demands = load_vrp_instance("instances\A\A-n32-k5.vrp")

# dist_matrix = get_distance_matrix(dimension, node_coords)

# # Função de custo
# def cost_function(route):
#     cost = 0.0
#     for route in solution:
#         if len(route) > 0:
#             for i in range(len(route)):
#                 if i < len(route) - 1:
#                     cost += dist_matrix[route[i] - 1][route[i+1] - 1]
#                 else:
#                     cost += dist_matrix[route[i] - 1][0]
#     return cost

# # Solução inicial: cada cliente é alocado em um veículo separado
# solution = [[i] for i in range(2, dimension + 1)]

# # Função para verificar se uma solução é viável
# def is_feasible(solution):
#     for route in solution:
#         total_demand = sum(demands[node] for node in route)
#         if total_demand > capacity:
#             return False
#     return True

# # Algoritmo de busca local - Troca de dois clientes entre rotas
# def local_search(solution):
#     best_solution = solution.copy()
#     best_cost = cost_function(solution)

#     for i in range(len(solution)):
#         for j in range(len(solution)):
#             if i == j: continue
#             for k in range(len(solution[i])):
#                 for l in range(len(solution[j])):
#                     new_solution = solution.copy()
#                     new_solution[i][k], new_solution[j][l] = new_solution[j][l], new_solution[i][k]
#                     if is_feasible(new_solution):
#                         cost = cost_function(new_solution)
#                         if cost < best_cost:
#                             best_solution = new_solution.copy()
#                             best_cost = cost

#     return best_solution

# def calculate_distance(coord1, coord2):
#     return np.linalg.norm(coord1 - coord2)

# def calculate_route_cost(route, distance_matrix):
#     cost = 0
#     for i in range(len(route) - 1):
#         start_node = route[i]
#         end_node = route[i+1]
#         cost += distance_matrix[start_node][end_node]
#     return cost


# def semi_greedy_cvrp(distance_matrix, demands, capacity, k_percentage, max_iterations):
#     num_customers = len(demands) - 1
#     num_vehicles = 0
#     optimal_value = 0
#     best_routes = []
    
#     # Calcular o valor de k baseado no percentual fornecido
#     k = int(num_customers * (k_percentage / 100))
    
#     # Iterações da heurística semi-gulosa
#     for iteration in range(max_iterations):
#         # Inicializar as rotas e as listas de clientes disponíveis e visitados
#         routes = []
#         available_customers = list(range(1, num_customers + 1))
#         visited_customers = []
        
#         # Criar uma rota inicial com um cliente aleatório
#         initial_customer = np.random.choice(available_customers)
#         current_route = [0, initial_customer]
#         available_customers.remove(initial_customer)
#         visited_customers.append(initial_customer)
        
#         # Construir as rotas usando a estratégia semi-gulosa
#         while available_customers:
#             current_customer = current_route[-1]
#             remaining_capacity = capacity - sum(demands.get(current_node,0) for current_node in current_route)
            
#             # Selecionar os k clientes mais próximos disponíveis
#             candidate_customers = []
#             for customer in available_customers:
#                 distance = distance_matrix[current_customer][customer]
#                 candidate_customers.append((customer, distance))
#             candidate_customers.sort(key=lambda x: x[1])
#             candidate_customers = candidate_customers[:k]
            
#             # Selecionar o próximo cliente baseado na demanda e na capacidade restante
#             next_customer = None
#             for customer, _ in candidate_customers:
#                 if demands[customer] <= remaining_capacity:
#                     next_customer = customer
#                     break
            
#             # Se nenhum cliente puder ser alocado, finalizar a rota atual
#             if next_customer is None:
#                 current_route.append(0)
#                 routes.append(current_route)
#                 current_route = [0]
#             else:
#                 current_route.append(next_customer)
#                 available_customers.remove(next_customer)
#                 visited_customers.append(next_customer)
        
#         # Adicionar a última rota gerada
#         current_route.append(0)
#         routes.append(current_route)
        
#         # Realizar a busca local em cada rota
#         improved_routes = []
#         for route in routes:
#             improved_route = local_search(route, distance_matrix, demands, capacity)
#             improved_routes.append(improved_route)
        
#         # Calcular o custo total das rotas
#         total_cost = sum(calculate_route_cost(route, distance_matrix) for route in improved_routes)
        
#         # Atualizar a melhor solução encontrada, se necessário
#         if num_vehicles == 0 or total_cost < optimal_value:
#             num_vehicles = len(improved_routes)
#             optimal_value = total_cost
#             best_routes = improved_routes

#     return num_vehicles, optimal_value, best_routes

        
# semi_greedy_cvrp(dist_matrix, demands, capacity, 50, 10000)


from construtiva_semi_gulosa import SemiGreedyCRVP
from iterated_greedy import IteratedGreedyCRVP


# semi_greedy = SemiGreedyCRVP()
# print(semi_greedy.run(5000, 50))

iterated_greedy = IteratedGreedyCRVP()
print(iterated_greedy.run(100, 50))


