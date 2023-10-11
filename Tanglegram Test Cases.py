from tanglegramClass import *


#for |T| = 2, |B| = 1. Completely solved: described by these 25 cases
leftTree = [BinaryTree(7, [[{0,1},{2,3,4,5,6}],[{0},{1}],[{2},{3,4,5,6}],[{3,4},{5,6}],[{3},{4}],[{5},{6}]]), BinaryTree(7, [[{0,1},{2,3,4,5,6}],[{0},{1}],[{2},{3,4,5,6}],[{3},{4,5,6}],[{4},{5,6}],[{5},{6}]]), BinaryTree(7, [[{0,1},{2,3,4,5,6}],[{0},{1}],[{2},{3,4,5,6}],[{3},{4,5,6}],[{4,5},{6}],[{4},{5}]]), BinaryTree(7, [[{0,1},{2,3,4,5,6}],[{0},{1}],[{2},{3,4,5,6}],[{3,4,5},{6}],[{3,4},{5}],[{3},{4}]]), BinaryTree(7, [[{0,1},{2,3,4,5,6}],[{0},{1}],[{2},{3,4,5,6}],[{3,4,5},{6}],[{3},{4,5}],[{4},{5}]])]
rightTree = [BinaryTree(7, [[{0,1,2,3,4,5},{6}],[{0,1,2,3,4},{5}],[{0,1,2,3},{4}],[{0,1},{2,3}],[{0},{1}], [{2},{3}]]), BinaryTree(7, [[{0,1,2,3,4,5},{6}],[{0,1,2,3,4},{5}],[{0,1,2,3},{4}],[{0},{1,2,3}],[{1},{2,3}], [{2},{3}]]),    BinaryTree(7, [[{0,1,2,3,4,5},{6}],[{0,1,2,3,4},{5}],[{0,1,2,3},{4}],[{0},{1,2,3}],[{1,2},{3}], [{1},{2}]]), BinaryTree(7, [[{0,1,2,3,4,5},{6}],[{0,1,2,3,4},{5}],[{0,1,2,3},{4}],[{0,1,2},{3}],[{0},{1,2}], [{1},{2}]]), BinaryTree(7, [[{0,1,2,3,4,5},{6}],[{0,1,2,3,4},{5}],[{0,1,2,3},{4}],[{0,1,2},{3}],[{0,1},{2}], [{0},{1}]])]
matching = [[0,0],[1,1],[2,4],[3,2],[4,3],[5,5], [6,6]]

Tanglegrams = []
for i in leftTree:
    for j in rightTree:
        Tanglegrams.append(Tanglegram(i,j,matching))

for T in Tanglegrams:
    print(T.isCrossingCritical())



"""
#case for |T| = 1, |B| = 1
leftTree = [BinaryTree(6, [[{0},{1,2,3,4,5}],[{1},{2,3,4,5}],[{2},{3,4,5}],[{3},{4,5}],[{4},{5}]])]
rightTree = [BinaryTree(6, [[{0,1,2,3,4},{5}],[{0,1,2,3},{4}],[{0,1,2},{3}],[{0,1},{2}],[{0},{1}]])]
matching = [[[0,0],[1,2],[2,1],[3,4],[4,3],[5,5]], [[0,0],[1,2],[2,4],[3,1],[4,3],[5,5]], [[0,0],[1,2],[2,4],[3,3],[4,1],[5,5]], [[0,0],[1,3],[2,1],[3,4],[4,2],[5,5]], [[0,0],[1,3],[2,2],[3,4],[4,1],[5,5]], [[0,0],[1,3],[2,4],[3,1],[4,2],[5,5]], [[0,0],[1,3],[2,4],[3,2],[4,1],[5,5]], [[0,0],[1,3],[2,4],[3,2],[4,1],[5,5]], [[0,0],[1,3],[2,4],[3,1],[4,2],[5,5]], [[0,0],[1,4],[2,1],[3,3],[4,2],[5,5]], [[0,0],[1,4],[2,2],[3,3],[4,1],[5,5]], [[0,0],[1,4],[2,3],[3,2],[4,1],[5,5]], [[0,0],[1,4],[2,3],[3,1],[4,2],[5,5]], [[0,0],[1,4],[2,3],[3,3],[4,2],[5,5]], [[0,0],[1,4],[2,2],[3,3],[4,1],[5,5]], [[0,0],[1,4],[2,3],[3,2],[4,1],[5,5]], [[0,0],[1,4],[2,3],[3,1],[4,2],[5,5]], [[0,0],[1,4],[2,2],[3,1],[4,3],[5,5]]]

Tanglegrams = []
for i in leftTree:
    for j in rightTree:
            for m in matching:
                Tanglegrams.append(Tanglegram(i,j,m))

for T in Tanglegrams:
    x = T.findCrossingNumber()
    if x < 2:
        print("Warning: ", T.sigma)
    print(x)
    """


#case b
leftTree = [BinaryTree(6, [[{0,1},{2,3,4,5}],[{0},{1}],[{2,3},{4,5}],[{2},{3}],[{4},{5}]])]
rightTree = [BinaryTree(6, [[{0,1,2,3},{4,5}],[{0,1},{2,3}],[{0},{1}],[{2},{3}],[{4},{5}]])]
matching = [[0,0],[1,2],[2,3],[3,4],[4,1],[5,5]]

Tanglegrams = []
for i in leftTree:
    for j in rightTree:
        Tanglegrams.append(Tanglegram(i,j,matching))

for T in Tanglegrams:
    print(T.findCrossingNumber())
    print(T.isCrossingCritical())