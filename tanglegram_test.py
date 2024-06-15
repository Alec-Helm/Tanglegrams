###make sure that starting from ((1),(1), {1:1}), we can generate all non-isomorphic tanglegrams
from tanglegram_class import create_binary_tree, generate_tanglegram_extensions_from_set, Tanglegram


Simplest_Tree = create_binary_tree('1')
Simplest_Matching = {'1':'1'}

Simplest_Tanglegram = Tanglegram(Simplest_Tree, Simplest_Tree, Simplest_Matching)
Current_Tanglegrams = [Simplest_Tanglegram]


for i in range(6):
    Current_Tanglegrams = generate_tanglegram_extensions_from_set(Current_Tanglegrams, str(i+2), str(i+2))

    print("There are " , len(Current_Tanglegrams), " distinct tanglegrams of size ", str(i+2))
    print()
