# 55MQU_vehicle_routing
O Problema de Roteamento de Veículos (Vehicle Routing Problem - VRP) é um problema de otimização combinatória que envolve determinar as rotas ótimas para uma frota de veículos atender a um conjunto de clientes, minimizando o custo total. No VRP, cada cliente tem uma demanda por bens ou serviços, e os veículos devem ser atribuídos aos clientes de modo que todas as demandas sejam satisfeitas e a distância total percorrida ou o número de veículos utilizados seja minimizado.

Todas instancias foram retiradas de: 
http://vrp.galgos.inf.puc-rio.br/index.php/en/

NAME: O nome do problema.
COMMENT: Um comentário ou descrição adicional sobre o problema.
TYPE: O tipo de problema, no caso, CVRP (Capacitated Vehicle Routing Problem - Problema de Roteamento de Veículos com Capacidade).
DIMENSION: O número total de nós (clientes + depósito).
EDGE_WEIGHT_TYPE: O tipo de métrica utilizada para calcular as distâncias entre os nós, no caso, EUC_2D (distância euclidiana em 2D).
CAPACITY: A capacidade máxima de cada veículo.
NODE_COORD_SECTION: A seção que define as coordenadas (x, y) de cada nó.
DEMAND_SECTION: A seção que define a demanda de cada nó (exceto o depósito).
DEPOT_SECTION: A seção que define o depósito.

solution: Uma lista que representa a solução do problema, onde cada elemento da lista é uma rota (uma lista de nós visitados) de um veículo. A solução inicial atribui cada cliente a um veículo separado.
node_coords: Um dicionário que armazena as coordenadas (x, y) de cada nó, incluindo o depósito.
demands: Um dicionário que armazena a demanda de cada nó (exceto o depósito).
dist_matrix: Uma matriz que armazena as distâncias entre todos os nós, calculadas com base nas coordenadas utilizando a métrica EUC_2D.
cost_function: Uma função que calcula o custo total de uma solução, somando as distâncias percorridas por cada veículo.
is_feasible: Uma função que verifica se uma solução é viável, ou seja, se a capacidade de cada veículo não é excedida.
print_solution: Uma função que imprime a solução encontrada, exibindo as rotas de cada veículo e o custo total.
local_search: O algoritmo de busca local que tenta melhorar a solução inicial trocando dois clientes entre rotas.
x_coords e y_coords: Listas que armazenam as coordenadas x e y dos nós para plotagem do gráfico.