"""tanglegram_class provides the ability to create 
 tanglegram objects out of binary trees and permutations.
 Tanglegrams are equipped with the ability to have their crossing number determined, 
 to report their size, and to determine if they are k-crossing critical for any given k"""

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


    def possible_canonical_orderings(self):
        """returns the leaf orderings in all possible canonical layouts
        as a frozenset of ordered tuples"""
        if self.n == 1:
            return frozenset((self.identity,))
        else:
            upper_orderings = self.upper_child.possible_orderings()
            upper_size = (self.upper_child).n
            lower_orderings = self.lower_child.possible_orderings()
            lower_size = (self.lower_child).n

            new_orderings = set()

            if upper_size >= lower_size:
                for i in upper_orderings:
                    for j in lower_orderings:
                        new_orderings.add(i+j)
            if upper_size <= lower_size:
                for i in upper_orderings:
                    for j in lower_orderings:
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


def binary_tree_ismorphic_check(binary_tree1, binary_tree2):
    """reports whether or not the two given binary trees are isomorphic"""

    if binary_tree1.n != binary_tree2.n:
        return False

    if binary_tree_ismorphic_check(binary_tree1.upper_child, binary_tree2.upper_child) and binary_tree_ismorphic_check(binary_tree1.lower_child, binary_tree2.lower_child):
        return True
    elif binary_tree_ismorphic_check(binary_tree1.upper_child, binary_tree2.lower_child) and binary_tree_ismorphic_check(binary_tree1.lower_child, binary_tree2.upper_child):
        return True
    else:
        return False

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

        return self



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


    def get_canonical_layouts(self):
        """returns a tuple where the first element is all canonical leaf
        orders of the left tree, and the second is all canonical
        leaf orders of the right tree"""
        return (self.L.possible_canonical_orderings(), self.R.possible_canonical_orderings())




def determine_isomorphic(tanglegram1, tanglegram2):
    """determines if there exists a tanglegram isomorphism
    between the two given tanglegram objects"""

    #first, make sure the left and right trees are actually isomorphic
    if not binary_tree_ismorphic_check(tanglegram1.L, tanglegram2.L):
        return False
    if not binary_tree_ismorphic_check(tanglegram1.R, tanglegram2.R):
        return False

    #first, pick an arbitrary canonical layout of tanglegram1
    fixed_layouts = tanglegram1.get_canonical_layouts()
    not_found = True
    for layout in fixed_layouts:
        if not_found:
            fixed_left = layout[0]
            fixed_right = layout[1]
            not_found = True

    #next find the permutation associated with the fixed layout
    matching1 = tanglegram1.sigma
    fixed_permutation = []
    for index in fixed_left:
        fixed_permutation.append(fixed_right.index(matching1[index]))


    #then get all layouts of tanglegram2
    comparison_layouts = tanglegram2.get_canonical_layouts()
    comparison_left_layouts = comparison_layouts[0]
    comparison_right_layouts = comparison_layouts[1]


    #then, check if they are isomorphic
    #by determining the associated permutation and seeing if its the same
    #as the fixed one
    matching2 = tanglegram2.sigma

    for index, left_layout in enumerate(comparison_left_layouts):
        counter = 0

        for left_leaf in left_layout:
            right_index = (comparison_right_layouts[index]).index(matching2[left_leaf])
            if right_index != fixed_permutation[counter]:
                break
            if counter == len(matching2):
                return True
            counter += 1

    return False
