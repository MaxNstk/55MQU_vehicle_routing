import numpy as np


def load_vrp_instance(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()

    instance_data = {}
    
    node_coords = {}
    demands = {}

    num_vehicles = int(file_path.split('/')[-1].split('-')[-1].split('.')[0][1:])

    for idx, line in enumerate(lines, start=1):
        line = line.strip()

        if line.startswith("COMMENT"):
            capacity = int(line.replace(')','').split(" ")[-1])
      
        elif line.startswith("DIMENSION"):
            optimal_value = int(line.split(" ")[-1])

        elif line.startswith("CAPACITY"):
            dimension = int(line.split(":")[1].strip())

        elif line.startswith("NODE_COORD_SECTION"):
            for i in range(dimension):
                node_info = lines[i + idx].split()
                node_coords[int(node_info[0])] = (float(node_info[1]), float(node_info[2]))

        elif line.startswith("DEMAND_SECTION"):
            for i in range(dimension):
                demand_info = lines[i + idx].split()
                demands[int(demand_info[0])] = int(demand_info[1])


    return capacity, num_vehicles, optimal_value, dimension, node_coords, demands


def get_distance_matrix(dimension, node_coords):

    # Monta matriz com as dimensões preenchidas com 0
    dist_matrix = np.zeros((dimension, dimension))

    # para todo nó calcula a distancia euclidiana entre todos os demais nós e põe na matriz
    for i in range(dimension):
        for j in range(dimension):
            if i == j: continue
            x1, y1 = node_coords[i+1]
            x2, y2 = node_coords[j+1]
            dist_matrix[i-1][j-1] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return dist_matrix