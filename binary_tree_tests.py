###make sure that starting from (1), we can generate all non-isomorphic binary trees
from tanglegram_class import create_binary_tree, generate_nonisomorphic_tree_extensions_from_set


current_trees = [create_binary_tree('1')]


for i in range(10):
    current_trees = generate_nonisomorphic_tree_extensions_from_set(current_trees, str(i+2))

    print("There are " , len(current_trees), " distinct rooted binary trees of size ", str(i+2))
    print()
