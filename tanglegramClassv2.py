import os
#create a tree from a parenthesized setup
def createBinaryTree(parenthesization):
    if not isinstance(parenthesization, tuple):
        parenthesization = (parenthesization,)
    length = len(parenthesization)
    if length == 1:
        return BT(1, parenthesization[0], parenthesization[0])
    else:
        left = createBinaryTree(parenthesization[0])
        right = createBinaryTree(parenthesization[1])
        return BT(length, left, right)




#to build a binary tree either (1) size > 1 and you provide the upper child tree and lower child tree or (2) size = 1 and childOne and childTwo should store the name of the leaf
class BT:
    def __init__(self, size, childOne, childTwo):
        self.n = size
        if size == 1:
            self.identity = (childOne,)
        else:
            self.upperChild = childOne
            self.lowerChild = childTwo
            self.identity = childOne.identity + childTwo.identity
        
    #removes the leaf with the given label from itself and all subtrees
    def removeLeaf(self, leafName):
        if leafName in self.identity:
            self.n -= 1
            if self.n > 0:
                prunedUpTree = self.upperChild.removeLeaf(leafName)
                if prunedUpTree == False:
                    self.identity = self.lowerChild.identity
                    return self.lowerChild

                prunedDownTree = self.lowerChild.removeLeaf(leafName)
                if prunedDownTree == False:
                    self.identity = self.upperChild.identity
                    return self.upperChild
                    
                self.identity = prunedUpTree.identity + prunedDownTree.identity
                return BT(self.n, prunedUpTree, prunedDownTree)

            else:
                return False
        else:
            return self
        
    #returns the leaf orderings in all possible layouts
    def possibleOrderings(self):
        if self.n == 1:
            return frozenset((self.identity,))
        else:
            upperOrderings = self.upperChild.possibleOrderings()
            lowerOrderings = self.lowerChild.possibleOrderings()

            newOrderings = set()
            for i in upperOrderings:
                for j in lowerOrderings:
                    newOrderings.add(i+j)
                    newOrderings.add(j+i)
            return frozenset(newOrderings)



#provide two binary trees and a matching between their vertices
#a matching should be a dictionary
class T:
    def __init__(self, left, right, matching):
        self.L = left
        self.R = right
        self.sigma = matching
        self.size = len(self.sigma)


    #finds the crossing number of the tanglegram naively by looking at all possible combinatorial layouts
    def crossingNumber(self):
        leftLayouts = self.L.possibleOrderings()
        rightLayouts = self.R.possibleOrderings()

        currentCrossingNumber = self.size*self.size 

        #progress up->down through the leaf order of the left tree
        #for each one, see which lower leaves have edges which cross it
        for left in leftLayouts:
            for right in rightLayouts:
                numCrossings = 0
                for i in range(self.size):

                    matchIndex = right.index(self.sigma[left[i]])
                    for j in range(i + 1, self.size):
                        lowerMatchIndex = right.index(self.sigma[left[j]])

                        if lowerMatchIndex < matchIndex:
                            numCrossings += 1
                if numCrossings < currentCrossingNumber:
                    currentCrossingNumber = numCrossings
        return currentCrossingNumber
    

    def TESTcrossingNumber(self):
        leftLayouts = self.L.possibleOrderings()
        rightLayouts = self.R.possibleOrderings()

        currentCrossingNumber = self.size**2

        #progress up->down through the leaf order of the left tree
        #for each one, see which lower leaves have edges which cross it
        for left in leftLayouts:
            for right in rightLayouts:

                numCrossings = 0


                for i in range(self.size):

                    matchIndex = right.index(self.sigma[left[i]])
                    for j in range(i + 1, self.size):
                        lowerMatchIndex = right.index(self.sigma[left[j]])

                        if lowerMatchIndex < matchIndex:
                            numCrossings += 1
                    
                if numCrossings <= 1:
                    print(left)
                    print(right)
                    print()
                    quit()
                if numCrossings < currentCrossingNumber:
                    currentCrossingNumber = numCrossings


        return currentCrossingNumber






    #def crossingCritical(self, k):





#for all given left-trees, right-trees, and matchings, checks that crossing number >= 2
def TwoCrossingChecker(leftTrees, rightTrees, matchings):
    for L in leftTrees:
        for R in rightTrees:
            for M in matchings:

                Tanglegram = T(createBinaryTree(L), createBinaryTree(R), M)
                if Tanglegram.crossingNumber()<= 1:
                    print("Uh Oh")
                    print(L)
                    print(R)
                    print()
                    print()
                    Tanglegram.TESTcrossingNumber()

