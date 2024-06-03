from tanglegram_class import *


L1 = create_binary_tree(((1,2),(3,4)))
L2 = create_binary_tree((1,(2,(3,4))))

R1 = create_binary_tree(((1,2),(3,4)))
R2 = create_binary_tree((((1,2),3),4))

print(R1.identity)

m1 = {1:1, 2:3, 3:2, 4:4}
m2 = {1:4, 2:3, 3:2, 4:1}

T1 = Tanglegram(L1, R1, m1)
T2 = Tanglegram(L2, R2, m1)
T3 = Tanglegram(L1, R1, m2)
T4 = Tanglegram(L2, R2, m2)

T = (T1, T2, T3, T4)

for t in T:
    print(t.crossing_number)
    print(t.is_crossing_critical(1))