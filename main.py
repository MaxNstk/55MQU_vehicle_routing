from construtiva_semi_gulosa import SemiGreedyCRVP
from semy_greedy_v2 import SemiGreedyCRVP2
# from iterated_greedy import IteratedGreedyCRVP

# instances = [
#     "instances\A\A-n32-k5.vrp", 
#     "instances\A\A-n45-k7.vrp",
#     "instances\A\A-n63-k10.vrp",
#     "instances\A\A-n65-k9.vrp",
#     "instances\A\A-n80-k10.vrp",
#     "instances\Uchoa_2014\X\X-n101-k25.vrp",
#     "instances\Uchoa_2014\X\X-n110-k13.vrp",
#     "instances\Uchoa_2014\X\X-n125-k30.vrp",
#     "instances\Uchoa_2014\X\X-n139-k10.vrp",
#     "instances\Uchoa_2014\X\X-n148-k46.vrp",
#     "instances\Uchoa_2014\X\X-n153-k22.vrp",
#     "instances\Uchoa_2014\X\X-n167-k10.vrp",
#     "instances\Uchoa_2014\X\X-n176-k26.vrp",
#     "instances\Uchoa_2014\X\X-n186-k15.vrp",
#     "instances\Uchoa_2014\X\X-n195-k51.vrp",
#     "instances\Uchoa_2014\X\X-n251-k28.vrp",
#     "instances\Uchoa_2014\X\X-n284-k15.vrp",
#     "instances\Uchoa_2014\X\X-n294-k50.vrp",
#     ]

semi_greedy = SemiGreedyCRVP2(file_path="instances\A\A-n32-k5.vrp")
print(semi_greedy.run(max_iterations=5000, k_percentage=50))

# iterated_greedy = IteratedGreedyCRVP(file_path="instances\A\A-n32-k5.vrp")
# print(iterated_greedy.run(max_iterations=5000, destruction_percentage=20))


