import random
import numpy as np

class VehicleRoutingProblem:

    best_routes = None
    best_cost = None
    
    current_routes = None
    current_routes_cost = None

    available_customers = None


    def __init__(self, file_path="instances\A\A-n32-k5.vrp"):
        self.file_path = file_path
        self.vehicle_capacity, self.num_vehicles, self.optimal_value, self.dimension, self.node_coords, self.demands = self.load_vrp_instance(file_path)
        self.dist_matrix = self.get_distance_matrix(self.dimension, self.node_coords)
    
    def get_closest_customers(self, current_customer, available_customers):
        closest_cutomers = []
        for customer in available_customers:
            distance = self.dist_matrix[current_customer-1][customer-1]
            closest_cutomers.append((customer, distance))
        closest_cutomers.sort(key=lambda x: x[1])
        return list(map(lambda x: x[0], closest_cutomers))

    def set_k_customers_amount(self,customers_amount):
        # para transformar o semi guloso em um guloso sete o percentual k para 0
        if self.k_percentage == 0:
            self.k = 1
        else:
            self.k = int(customers_amount * (self.k_percentage / 100))
            self.k = 1 if not self.k else self.k

    def get_empty_routes(self):
        # Cria a quantidade de rotas referente a quantidade de veículos e adiciona o depósito nela
        return [[1] for _ in range(self.num_vehicles)]
    
    def get_all_customers(self):
        # inicializa a lista de clientes disponiveis, a partir do 2 (0 não exite e 1 é o depósito) ate o ultimo
       return list(range(2, len(self.demands)+1))
    
    def add_deposit_to_routes(self,routes):
        for route in routes:
            if route[-1] != 1:
                route.append(1) 

    def get_remaining_capacity(self, route):
        return self.vehicle_capacity - sum(self.demands[node] for node in route)
    
    def get_route_with_more_capacity(self, routes):
        capacities = [self.get_remaining_capacity(route) for route in routes]
        return routes[capacities.index(max(capacities))]
    
    def get_random_route(self):
        return self.current_routes[random.randint(0, (self.num_vehicles)-1)]

    def run(self):
        raise NotImplementedError()
    
    def get_routes_cost(self, solution):
        return sum(self.calculate_route_cost(node, self.dist_matrix) for node in solution)
    
    def load_vrp_instance(self, file_path):

        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        node_coords = {}
        demands = {}

        num_vehicles = int(file_path.split('/')[-1].split('-')[-1].split('.')[0][1:])

        for idx, line in enumerate(lines, start=1):
            line = line.strip()

            if line.startswith("COMMENT"):
                optimal_value = int(line.replace(')','').split(" ")[-1])
        
            elif line.startswith("DIMENSION"):
                dimension = int(line.split(" ")[-1])

            elif line.startswith("CAPACITY"):
                capacity = int(line.split(":")[1].strip())

            elif line.startswith("NODE_COORD_SECTION"):
                for i in range(dimension):
                    node_info = lines[i + idx].split()
                    node_coords[int(node_info[0])] = (float(node_info[1]), float(node_info[2]))

            elif line.startswith("DEMAND_SECTION"):
                for i in range(dimension):
                    demand_info = lines[i + idx].split()
                    demands[int(demand_info[0])] = int(demand_info[1])


        return capacity, num_vehicles, optimal_value, dimension, node_coords, demands


    def get_distance_matrix(self, dimension, node_coords):

        # Monta matriz com as dimensões preenchidas com 0
        dist_matrix = np.zeros((dimension, dimension))

        # para todo nó calcula a distancia euclidiana entre todos os demais nós e põe na matriz
        for i in range(dimension):
            x1, y1 = node_coords[i+1]
            for j in range(dimension):
                if i == j: continue
                x2, y2 = node_coords[j+1]
                dist_matrix[i-1][j-1] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        return dist_matrix

    def get_distance_from_origin(self, x, y):
            return np.sqrt((x)**2 + (y)**2)


    def calculate_route_cost(self, route, distance_matrix):
        cost = 0
        for i in range(len(route) - 1):
            start_node = route[i]
            end_node = route[i+1]
            cost += distance_matrix[start_node-1][end_node-1]
        return cost