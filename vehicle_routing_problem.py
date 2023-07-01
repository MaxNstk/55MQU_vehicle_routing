from utils import get_distance_matrix, load_vrp_instance

class VehicleRoutingProblem:

    def __init__(self, file_path="instances\A\A-n32-k5.vrp"):
        self.file_path = file_path
        self.vehicle_capacity, self.num_vehicles, self.optimal_value, self.dimension, self.node_coords, self.demands = load_vrp_instance(file_path)
        self.dist_matrix = get_distance_matrix(self.dimension, self.node_coords)

    def run(self):
        raise NotImplementedError()