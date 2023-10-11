from itertools import permutations

#little global helper class
def get_powerset(some_list):
    """Returns all subsets of size 0 - len(some_list) for some_list"""
    if len(some_list) == 0:
        return [[]]

    subsets = []
    first_element = some_list[0]
    remaining_list = some_list[1:]
    # Strategy: get all the subsets of remaining_list. For each
    # of those subsets, a full subset list will contain both
    # the original subset as well as a version of the subset
    # that contains first_element
    for partial_subset in get_powerset(remaining_list):
        subsets.append(partial_subset)
        subsets.append(partial_subset[:] + [first_element])

    return subsets

#recursively generate all binary trees on 'n' leaves in canonical layout
#by canonical, it means that at every internal vertex the up-tree is no smaller than the down-tree
def canonicalBinaryTreeGenerator(numLeaves):
    internalVertices = canonicalBinaryTreeGeneratorIterator(range(numLeaves))
    fullTreeList = []

    for i in internalVertices:
        newTree = BinaryTree(numLeaves, i)
        fullTreeList.append(newTree)
    
    return fullTreeList

def canonicalBinaryTreeGeneratorIterator(leafList):
    treeList = []
    numLeaves = len(leafList)

    if numLeaves == 1:
        return []
    else:
        halfwayPoint = (numLeaves + 1) // 2

        for firstDownLeaf in range(halfwayPoint, numLeaves):
            
            upTreeLeaves = leafList[0:firstDownLeaf]
            downTreeLeaves = leafList[firstDownLeaf:]

            internalVertex = [[set(upTreeLeaves), set(downTreeLeaves)]]
            possibleUpTrees = canonicalBinaryTreeGeneratorIterator(upTreeLeaves)
            possibleDownTrees = canonicalBinaryTreeGeneratorIterator(downTreeLeaves)

            if len(possibleUpTrees)  == 0:
                if len(possibleDownTrees) == 0:
                    treeList.append(internalVertex)
                else: 
                    for j in possibleDownTrees:
                        treeList.append((internalVertex + j))

            else:
                if len(possibleDownTrees) == 0:
                    for i in possibleUpTrees:
                        treeList.append((internalVertex + i))
                else: 
                    for i in possibleUpTrees:
                        for j in possibleDownTrees:
                            treeList.append((internalVertex + i + j))
        
        return treeList

    


#a tree is really just a set [0,1,2,...,n-1] (the leaves) and a set of permutations (internal vertices)
class BinaryTree:
    def __init__(self, size, permutations):
        self.size = size
        self.permutations = permutations
        

    #looks at the index of the permutation and changes the ordering of the leaves appropriately
    #permutations should be a list with entries like [upLeafSet, downLeafSet] where upLeafSet and downLeafSet are sets
    def permuteTree(self, permutationIndecies):
        ordering = list(range(self.size))

        for i in permutationIndecies:
            ordering = self.switch(ordering,i)

        return(ordering)

    #performs a single switch given current ordering state and index of permutation
    def switch(self,ordering,permutationIndex):
        newOrdering = []

        permutation = self.permutations[permutationIndex]

        foundUpset = False
        currentIndex= 0


        while not foundUpset:

            
            if ordering[currentIndex] in permutation[0]:
                foundUpset = True
            else:
                newOrdering.append(ordering[currentIndex])
                currentIndex += 1

        moveDown = ordering[currentIndex: currentIndex + len(permutation[0])]
        moveUp = ordering[currentIndex + len(permutation[0]): currentIndex + len(permutation[0]) + len(permutation[1])]
        newOrdering = newOrdering + moveUp + moveDown
        currentIndex = currentIndex + len(permutation[0]) + len(permutation[1])

        while currentIndex < self.size:
            newOrdering.append(ordering[currentIndex])
            currentIndex += 1


        return newOrdering
    
    #a layout is just an ordering of the leaves
    def generateLayouts(self):
        fullPermutationIndexList = get_powerset(list(range(len(self.permutations))))
        layouts = []

        for permutationIndex in fullPermutationIndexList:
            layouts.append(self.permuteTree(permutationIndex))

        return layouts


    def generateTaggedLayouts(self):
        fullPermutationIndexList = get_powerset(list(range(len(self.permutations))))
        layouts = []

        for permutationIndex in fullPermutationIndexList:
            layouts.append([self.permuteTree(permutationIndex), permutationIndex])

        return layouts
    


    #remove a single leaf and supress the attatched internal vertex
    def removeLeaf(self, leafLabel):
        
        size = self.size

        #go through the tree and 
        # (1) remove  the unique vertex where the removed leaf splits off
        # (2) remove the leaf from all other internal vertices
        internalVertices = self.permutations


        newPermutations = []
        for i in internalVertices:
            upTree = i[0]
            downTree = i[1]

            newUpTree = set()
            newDownTree = set()

            for l in upTree:
                if l < leafLabel:
                    newUpTree.add(l)
                elif l > leafLabel:
                    newUpTree.add((l-1))

            for l in downTree:
                if l < leafLabel:
                    newDownTree.add(l)
                elif l > leafLabel:
                    newDownTree.add((l-1))

            if (len(newUpTree) != 0) and (len(newDownTree) != 0):
                newPermutations.append([newUpTree, newDownTree])

        prunedTree = BinaryTree( (size - 1), newPermutations)  
        return prunedTree

       
#generate list of all matchings of size n
def generateMatchings(n):
    numbers = list(range(1, n + 1))
    all_lists = []
    for perm in permutations(numbers):
        pair_list = [[x-1, y-1] for x, y in zip(numbers, perm)]
        if pair_list not in all_lists:
            all_lists.append(pair_list)
    return all_lists


#left and right tree should be BinaryTrees, matching is a list of list-pairs
class Tanglegram:
    def __init__(self, leftTree, rightTree, matching):
        self.L = leftTree
        self.R = rightTree
        self.sigma = matching

    #to find the tanglegram crossing number, we need to look at all layouts and select the minimum crossing number therein
    def findCrossingNumber(self):
        #start with an acceptable upper bound
        crossingNumber = (self.L.size)*(self.R.size)

        #generate all layouts of each tree
        leftLayouts = self.L.generateLayouts()
        rightLayouts = self.R.generateLayouts()

        for left in leftLayouts:
            for right in rightLayouts:
                numberCrossings = self.countCrossings(left, right)

                if numberCrossings < crossingNumber:
                    crossingNumber = numberCrossings

        return crossingNumber

    
    def countCrossings(self, leftLayout, rightLayout):
        numCrossings = 0
        
        matchingTabulator = [1]*len(leftLayout)

        for leftLeaf in range(len(leftLayout)):
            leftLeafLabel = leftLayout[leftLeaf]

            #find the label of the leaf matched on the right
            foundRightLabel = False
            rightLabelCounter = 0
            while not foundRightLabel:
                if self.sigma[rightLabelCounter][0] == leftLeafLabel:
                    rightLeafLabel = self.sigma[rightLabelCounter][1]
                    foundRightLabel = True
                else:
                    rightLabelCounter += 1

            #now we add the number of crossings this guy generates and remove the '1' from the tabulator
            tabulatorCounter = 0
            while rightLayout[tabulatorCounter] != rightLeafLabel:
                numCrossings += matchingTabulator[tabulatorCounter]
                tabulatorCounter += 1
            matchingTabulator[tabulatorCounter] = 0

        return numCrossings
    
    #same thing as finding crossing number, but keep a record of the premutations used to arrive at the best one
    def findOptimalLayout(self):
         #start with an acceptable upper bound
        crossingNumber = (self.L.size)*(self.R.size)
        optimalLayout = []

        #generate all layouts of each tree
        leftLayouts = self.L.generateTaggedLayouts()
        rightLayouts = self.R.generateTaggedLayouts()

        for left in leftLayouts:
            for right in rightLayouts:
                numberCrossings = self.countCrossings(left[0], right[0])

                if numberCrossings < crossingNumber:
                    crossingNumber = numberCrossings
                    optimalLayout = [left[1],right[1]]
                    treeOrderings = [left[0], right[0]]

        return [crossingNumber, optimalLayout, treeOrderings]
    

    #creates an induced subtanglegram with a single matching edge removed
    def removeEdge(self, leftLabel):
        originalLeftTree = self.L
        originalRightTree = self.R
        originalMatchings = self.sigma

        #find the label on the right tree to remove
        rightLabelFound = False
        rightLabel = -1
        while rightLabelFound == False:
            rightLabel += 1
            if leftLabel == originalMatchings[rightLabel][0]:
                rightLabel = originalMatchings[rightLabel][1]
                rightLabelFound = True

        #find the new left and right trees
        newLeftTree = originalLeftTree.removeLeaf(leftLabel)
        newRightTree = originalRightTree.removeLeaf(rightLabel)

        #prune the matching set
        newMatchings = []
        
        for e in originalMatchings:
            newMatching = []

            if e[0]< leftLabel:
                newMatching.append(e[0])
            elif e[0] > leftLabel:
                newMatching.append(e[0]-1)


            if e[1]< rightLabel:
                newMatching.append(e[1])
            elif e[1] > rightLabel:
                newMatching.append(e[1]-1)

            if len(newMatching) != 0:
                newMatchings.append(newMatching)

        #create the new tanglegram
        newTanglegram = Tanglegram(newLeftTree, newRightTree, newMatchings)
        return newTanglegram
        

    
    #finds its crossing number then looks at each sub-tanglegram with one edge removed to make sure the crossing number dropped
    def isCrossingCritical(self):
        #find crossing number
        crossingNumber = self.findCrossingNumber()
        crossingCritical = True

        #iterate through all subtanglegrams from removing one edge and check their crossing number
        for leafLabel in range(self.L.size):
            subtangle = self.removeEdge(leafLabel)
            reducedCrossingNumber = subtangle.findCrossingNumber()

            if reducedCrossingNumber == crossingNumber:
                crossingCritical = False
                

        return crossingCritical