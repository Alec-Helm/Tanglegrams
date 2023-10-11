from tanglegramClass import *


treesOnLeaves = []

nextSet = []




for i in [1,2,3,4,5,6,7]:
    print(i)
    trees = canonicalBinaryTreeGenerator(i+1)
    edges = generateMatchings(i+1)


    for L in trees:
        for R in trees:
            for sigma in edges:
                T = Tanglegram(L,R,sigma)
                if T.findCrossingNumber() == 2 and T.isCrossingCritical():
                    print(True)
                    print(L.permutations)
                    print(R.permutations)
                    print(sigma)
                    print(len(sigma))
                    print()
                    break
   