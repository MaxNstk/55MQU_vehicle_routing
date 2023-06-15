import numpy as np

def calculate_distance(coord1, coord2):
    return np.linalg.norm(coord1 - coord2)
    

def semi_greedy_cvrp(distance_matrix, demands, capacity, k_percentage, max_iterations):
    num_customers = len(demands) - 1
    num_vehicles = 0
    optimal_value = 0
    best_routes = []
    
    # Calcular o valor de k baseado no percentual fornecido
    k = int(num_customers * (k_percentage / 100))
    
    # Iterações da heurística semi-gulosa
    for iteration in range(max_iterations):
        # Inicializar as rotas e as listas de clientes disponíveis e visitados
        routes = []
        available_customers = list(range(1, num_customers + 1))
        visited_customers = []
        
        # Criar uma rota inicial com um cliente aleatório
        initial_customer = np.random.choice(available_customers)
        current_route = [0, initial_customer]
        available_customers.remove(initial_customer)
        visited_customers.append(initial_customer)
        
        # Construir as rotas usando a estratégia semi-gulosa
        while available_customers:
            current_customer = current_route[-1]
            remaining_capacity = capacity - sum(demands[current_route])
            
            # Selecionar os k clientes mais próximos disponíveis
            candidate_customers = []
            for customer in available_customers:
                distance = distance_matrix[current_customer][customer]
                candidate_customers.append((customer, distance))
            candidate_customers.sort(key=lambda x: x[1])
            candidate_customers = candidate_customers[:k]
            
            # Selecionar o próximo cliente baseado na demanda e na capacidade restante
            next_customer = None
            for customer, _ in candidate_customers:
                if demands[customer] <= remaining_capacity:
                    next_customer = customer
                    break
            
            # Se nenhum cliente puder ser alocado, finalizar a rota atual
            if next_customer is None:
                current_route.append(0)
                routes.append(current_route)
                current_route = [0]
            else:
                current_route.append(next_customer)
                available_customers.remove(next_customer)
                visited_customers.append(next_customer)
        
        # Adicionar a última rota gerada
        current_route.append(0)
        routes.append(current_route)
        
        # Realizar a busca local em cada rota
        improved_routes = []
        for route in routes:
            improved_route = local_search(route, distance_matrix, demands, capacity)
            improved_routes.append(improved_route)
        
        # Calcular o custo total das rotas
        total_cost = sum(calculate_route_cost(route, distance_matrix) for route in improved_routes)
        
        # Atualizar a melhor solução encontrada, se necessário
        if num_vehicles == 0 or total_cost < optimal_value:
            num_vehicles = len(improved_routes)
            optimal_value = total_cost
            best_routes = improved_routes
        
