"""tanglegram_class provides the ability to create 
 tanglegram objects out of binary trees and permutations.
 Tanglegrams are equipped with the ability to have their crossing number determined, 
 to report their size, and to determine if they are k-crossing critical for any given k"""

import copy




class BinaryTree:
    """binary_tree allows the creation of binary tree objects.
    these are created recursively by making cherries
    where leaves of the cherry can themselves be binary trees"""


    def __init__(self, size, child_one, child_two):
        """to build a binary tree provide either
        (1) size > 1 and you provide the upper child tree and lower child tree or 
        (2) size = 1 and childOne and childTwo should store the name of the leaf
        
        The identity of the tree is a possible leaf order as a tuple"""
        self.n = size
        if size == 1:
            self.identity = (child_one,)
        else:
            self.upper_child = child_one
            self.lower_child = child_two
            self.identity = child_one.identity + child_two.identity

    def remove_leaf(self, leaf_name):
        """removes the leaf with the given label from itself and all subtrees
        effectively resulting in the induced binary subtree on all other leaves"""
        if leaf_name in self.identity:
            self.n -= 1
            if self.n > 0:
                pruned_up_tree = self.upper_child.remove_leaf(leaf_name)
                if pruned_up_tree is False:
                    self.identity = self.lower_child.identity
                    return self.lower_child

                pruned_down_tree = self.lower_child.remove_leaf(leaf_name)
                if pruned_down_tree  is False:
                    self.identity = self.upper_child.identity
                    return self.upper_child
                    
                self.identity = pruned_up_tree.identity + pruned_down_tree.identity
                return BinaryTree(self.n, pruned_up_tree, pruned_down_tree)

            else:
                return False
        else:
            return self

    def possible_orderings(self):
        """returns the leaf orderings in all possible layouts
        as a frozenset of ordered tuples"""
        if self.n == 1:
            return frozenset((self.identity,))
        else:
            upper_orderings = self.upper_child.possible_orderings()
            lower_orderings = self.lower_child.possible_orderings()

            new_orderings = set()
            for i in upper_orderings:
                for j in lower_orderings:
                    new_orderings.add(i+j)
                    new_orderings.add(j+i)
            return frozenset(new_orderings)




def create_binary_tree(parenthesization):
    """create a BT object from a parenthesized setup: example, (a,(b,((c,d),e)))
    You may also supply other BT as input characters.
    Each internal pair of parentheses is itself a BT"""

    if not isinstance(parenthesization, tuple):
        parenthesization = (parenthesization,)

    length = len(parenthesization)
    if length == 1:
        return BinaryTree(1, parenthesization[0], parenthesization[0])
    else:
        left = create_binary_tree(parenthesization[0])
        right = create_binary_tree(parenthesization[1])
        return BinaryTree(length, left, right)




#provide two binary trees and a matching between their vertices
#a matching should be a dictionary
class Tanglegram:
    """creates a tanglegram object by providing two BinaryTrees
    and a matching between their leaves.
    The matching should be as a dictionary."""

    def __init__(self, left, right, matching):
        self.L = left
        self.R = right
        self.sigma = matching
        self.size = len(self.sigma)
        self.crossing_number = self.get_crossing_number()


    def get_crossing_number(self):
        """finds the crossing number of the tanglegram naively 
        by looking at all possible combinatorial layouts"""
        left_layouts = self.L.possible_orderings()
        right_layouts = self.R.possible_orderings()

        #sets a naive upper-bound on the crossing number
        current_crossing_number = self.size*self.size

        #progress up->down through the leaf order of the left tree
        #for each one, see which lower leaves have edges which cross it
        for left in left_layouts:
            for right in right_layouts:
                num_crossings = 0

                for index in range(self.size):
                    left_leaf = left[index]
                    right_leaf = self.sigma[left_leaf]

                    match_index = right.index(right_leaf)

                    for j in range(index + 1, self.size):
                        lower_match_index = right.index(self.sigma[left[j]])

                        if lower_match_index < match_index:
                            num_crossings += 1

                if num_crossings < current_crossing_number:
                    current_crossing_number = num_crossings

        return current_crossing_number

    def remove_matching(self, left_leaf):
        """removes the matching edge with given left leaf
        returns the original tanglegram if left leaf is not present"""

        if left_leaf not in (self.L).identity:
            return self

        (self.L).remove_leaf(left_leaf)
        (self.R).remove_leaf(self.sigma[left_leaf])
        (self.sigma).pop(left_leaf)
        self.size -= 1
        self.crossing_number = self.get_crossing_number



    def is_crossing_critical(self, k):
        """determines if the tanglegram is crossing-critical for given crossing number k"""

        #first, determine if the crossing number is at least k
        if self.crossing_number < k:
            return False

        #if the tanglegram is crossing critical, then every matching edge
        #must have some corresponding layout where if the edge is removed
        #the sub-layout has crossing number less than k
        #so we need to find such a layout for each edge
        found_checker = [0] * self.size
        num_found = 0

        #carefully determine the crossing number for each potential layout
        #in doing so, we count the responsibility of each matching edge
        #this allows us to determine the crossing number of the subtanglegram formed
        #by removing the matching edge

        #for each tanglegram, if an edge has not found a witnessing layout
        #we see if the crossing number drops below k be removing the edge

        left_layouts = self.L.possible_orderings()
        right_layouts = self.R.possible_orderings()


        #check each potential pair of binary tree layouts
        for left in left_layouts:
            for right in right_layouts:
                #make a list to hold the responsibility of each matching edge
                responsibility_tuple = [0] * (self.size)

                #count the total number of crossings
                num_crossings = 0

                #pick all possible pairs of left-indices
                #then see if the corresponding edges cross
                #in each case j < i, so they cross iff match_i < match_j
                for i in range(self.size):
                    for j in range(0,i):
                        match_i = right.index(self.sigma[left[i]])
                        match_j = right.index(self.sigma[left[j]])

                        if match_i < match_j:
                            num_crossings += 1
                            responsibility_tuple[i] += 1
                            responsibility_tuple[j] += 1

                #now for each un-witness edge, see if removing it drops the crossing number enough
                for i in range(self.size):
                    if found_checker[i] == 0:
                        if (num_crossings - responsibility_tuple[i]) < k:
                            num_found += 1
                            found_checker[i] = 1
                if num_found == self.size:
                    return True
        return False







