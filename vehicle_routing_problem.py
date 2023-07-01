from utils import get_distance_matrix, load_vrp_instance

class VehicleRoutingProblem:

    def __init__(self, file_path="instances\A\A-n32-k5.vrp"):
        self.file_path = file_path
        self.vehicle_capacity, self.num_vehicles, self.optimal_value, self.dimension, self.node_coords, self.demands = load_vrp_instance(file_path)
        self.dist_matrix = get_distance_matrix(self.dimension, self.node_coords)
    
    def get_closest_customers(self, current_customer, available_customers):
        closest_cutomers = []
        for customer in available_customers:
            distance = self.dist_matrix[current_customer-1][customer-1]
            closest_cutomers.append((customer, distance))
        closest_cutomers.sort(key=lambda x: x[1])
        return closest_cutomers

    def get_remaining_capacity(self, route):
        return self.vehicle_capacity - sum(self.demands[node] for node in route)

    def run(self):
        raise NotImplementedError()