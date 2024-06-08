from tanglegram_class import *

K1L = create_binary_tree(((1,2),(3,4)))
K2L = create_binary_tree((1,(2,(3,4))))

K1R = create_binary_tree(((1,2),(3,4)))
K2R = create_binary_tree((((1,2),3),4))

M = {1:1, 2:3, 3:2, 4:4}

K1 = Tanglegram(K1L, K1R, M)
K2 = Tanglegram(K2L, K2R, M)

print(check_canonical(K1L))
print(check_canonical(K2L))
print(check_canonical(K1R))
print(check_canonical(K2R))



T = (K1, K2)

for t in T:
    print(t.crossing_number)
    print(t.is_crossing_critical(1))