from vehicle_routing_problem import VehicleRoutingProblem
import random


class IteratedGreedyCRVP(VehicleRoutingProblem):

    """ Construtiva semi gulosa, preenche um caminhão de cada vez, 
    melhorar para verificar em qual caminhão deve ser posto """        
    
    def get_next_customer(self, customers, capacity):
        next_customer = None
        for customer in customers:
            if self.demands[customer] <= capacity:
                return customer     
        return next_customer
    
    def destroy(self):
        # remove elementos aleatórios das rotas, dado o parametro K
        idxs_to_remove = random.sample(range(len(self.visited_customers)), self.D)
        for index in sorted(idxs_to_remove, reverse=True):
            self.available_customers.append(self.visited_customers[index])
            del self.visited_customers[index]
        
        for idx, route in enumerate(self.current_routes):
            new_route = [customer for customer in route if route in self.visited_customers]                   
            self.current_routes[idx] = new_route

    def set_desctruction_amount(self, destruction_percentage):
        self.D = int((len(self.demands)-1) * (destruction_percentage / 100))
        self.D = 1 if not self.D else self.D
    
    def get_greedy_routes(self):   

        # Inicializar as rotas caso não venham por parâmetro
        if not self.current_routes: 
            self.current_routes = [[1] for _ in range(self.num_vehicles)]
            self.available_customers = list(range(2, len(self.demands)+1))
            self.visited_customers = []
            self.current_route = self.current_routes[0]
            
        while self.available_customers:        
            self.max_iterations -= 1

            # seleciona os mais próximos
            candidate_customers = self.get_closest_customers(self.current_route[-1], self.available_customers)

            # pega o com a menor rota
            next_customer = self.get_next_customer(candidate_customers, self.get_remaining_capacity(self.current_route))

            # caso não haja proximo cliente disponivel para rota, escolhemos outra aleatoriamente para utilizar
            if not next_customer:
                self.current_route = self.current_routes[random.randint(0, (self.num_vehicles)-1)]
                continue

            # adiciona o cliente na rota atual
            self.current_route.append(next_customer)
            self.available_customers.remove(next_customer)
            self.visited_customers.append(next_customer)

            # seleciona a rota baseado naquela que contem o menor numero de clientes
            self.current_route = min(self.current_routes, key=len)           
        
        for route in self.current_routes:
            route.append(1)

        self.current_routes_cost = self.calculate_solution_cost(self.current_routes)
        if not self.best_routes or self.current_routes_cost < self.best_cost:
            self.best_routes, self.best_cost = self.current_routes, self.current_routes_cost
        self.current_routes, self.current_routes_cost = self.best_routes, self.best_cost


    def run(self, max_iterations, destruction_percentage, force_solution=False):
        self.set_desctruction_amount(destruction_percentage)

        self.max_iterations = max_iterations

        for iteration in range(self.max_iterations):
            self.get_greedy_routes()   
            if self.best_cost == self.optimal_value:
                break
            self.destroy()
                     
        return self.best_routes, self.best_cost, self.optimal_value

semi_greedy = IteratedGreedyCRVP(file_path="instances\A\A-n32-k5.vrp")
print(semi_greedy.run(max_iterations=300, destruction_percentage=20))