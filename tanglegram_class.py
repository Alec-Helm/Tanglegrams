"""tanglegram_class provides the ability to create 
 tanglegram objects out of binary trees and permutations.
 Tanglegrams are equipped with the ability to have their crossing number determined, 
 to report their size, and to determine if they are k-crossing critical for any given k"""
# pylint: disable=line-too-long
import time


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
        as a list of ordered tuples"""
        if self.n == 1:
            return [self.identity]
        else:
            upper_orderings = self.upper_child.possible_orderings()
            lower_orderings = self.lower_child.possible_orderings()

            new_orderings = []
            for i in upper_orderings:
                for j in lower_orderings:
                    new_orderings.append(i+j)
                    new_orderings.append(j+i)
            return new_orderings


    def possible_canonical_orderings(self):
        """returns the leaf orderings in all possible canonical layouts
        as a parameter of ordered tuples"""
        if self.n == 1:
            return [self.identity]
        else:
            upper_orderings = self.upper_child.possible_canonical_orderings()
            upper_size = (self.upper_child).n
            lower_orderings = self.lower_child.possible_canonical_orderings()
            lower_size = (self.lower_child).n

            new_orderings = []

            if upper_size >= lower_size:
                for i in upper_orderings:
                    for j in lower_orderings:
                        new_orderings.append(i+j)
            if upper_size <= lower_size:
                for i in upper_orderings:
                    for j in lower_orderings:
                        new_orderings.append(j+i)

            return new_orderings







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

    #if both trees are size one, they are trivially isomorphic
    if binary_tree1.n == 1:
        return True

    if binary_tree_ismorphic_check(binary_tree1.upper_child, binary_tree2.upper_child) and binary_tree_ismorphic_check(binary_tree1.lower_child, binary_tree2.lower_child):
        return True
    if binary_tree_ismorphic_check(binary_tree1.upper_child, binary_tree2.lower_child) and binary_tree_ismorphic_check(binary_tree1.lower_child, binary_tree2.upper_child):
        return True
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

        return self



    def is_crossing_critical(self, k):
        """determines if the tanglegram is crossing-critical for given crossing number k"""

        #first, determine if the crossing number is at least k
        if self.get_crossing_number() < k:
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
        return [self.L.possible_canonical_orderings(), self.R.possible_canonical_orderings()]















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
    fixed_left = fixed_layouts[0][0]
    fixed_right = fixed_layouts[1][0]


    #next find the permutation associated with the fixed layout
    fixed_permutation = []
    for i in fixed_left:
        fixed_permutation.append(fixed_right.index((tanglegram1.sigma)[i]))


    #then get all layouts of tanglegram2
    comparison_layouts = tanglegram2.get_canonical_layouts()
    comparison_left_layouts = comparison_layouts[0]
    comparison_right_layouts = comparison_layouts[1]


    #then, check if they are isomorphic
    #by determining the associated permutation and seeing if its the same
    #as the fixed one
    for left_layout in comparison_left_layouts:
        for right_layout in comparison_right_layouts:
            counter = 0

            for left_leaf in left_layout:

                right_index = right_layout.index((tanglegram2.sigma)[left_leaf])
                if right_index != fixed_permutation[counter]:
                    break
                counter += 1
                if counter == len((tanglegram2.sigma)):
                    return True


    return False






def determine_isomorphic_assuming_trees_checked(tanglegram1, tanglegram2):
    """determines if there exists a tanglegram isomorphism
    between the two given tanglegram objects given the fact that the
    left and right trees are isomorphic"""


    #first, pick an arbitrary canonical layout of tanglegram1
    fixed_layouts = tanglegram1.get_canonical_layouts()
    fixed_left = fixed_layouts[0][0]
    fixed_right = fixed_layouts[1][0]


    #next find the permutation associated with the fixed layout
    fixed_permutation = []
    for i in fixed_left:
        fixed_permutation.append(fixed_right.index((tanglegram1.sigma)[i]))


    #then get all layouts of tanglegram2
    comparison_layouts = tanglegram2.get_canonical_layouts()
    comparison_left_layouts = comparison_layouts[0]
    comparison_right_layouts = comparison_layouts[1]


    #then, check if they are isomorphic
    #by determining the associated permutation and seeing if its the same
    #as the fixed one
    for left_layout in comparison_left_layouts:
        for right_layout in comparison_right_layouts:
            counter = 0

            for left_leaf in left_layout:

                right_index = right_layout.index((tanglegram2.sigma)[left_leaf])
                if right_index != fixed_permutation[counter]:
                    break
                counter += 1
                if counter == len((tanglegram2.sigma)):
                    return True


    return False



def generate_all_tree_extensions(binary_tree, new_leaf):
    """given a size n binary tree as input, generate all binary trees
    of size n+1 with the given binary tree as a sub-tree
    by adding a single leaf in all possible ways
    and then clearing by appeal to isomorphism"""

    new_binary_trees = []
    n = binary_tree.n + 1

    #we can add the new leaf such that it is a direct descendant of the root
    new_binary_trees.append(BinaryTree(n, binary_tree, create_binary_tree(new_leaf)))


    if binary_tree.n != 1:
        #we can add the new leaf to the upper child if the tree is non-singleton
        new_binary_trees.extend([BinaryTree(n, upper_child, binary_tree.lower_child) for upper_child in generate_all_tree_extensions(binary_tree.upper_child, new_leaf)])

        #or we can add the new leaf to the lower child
        new_binary_trees.extend([BinaryTree(n, binary_tree.upper_child, lower_child) for lower_child in generate_all_tree_extensions(binary_tree.lower_child, new_leaf)])

    return new_binary_trees


def generate_nonisomorphic_tree_extensions_from_set(binary_tree_set, new_leaf):
    """given a list of binary trees we extend each by the new leaf, then
    clear for isomorphisms"""
    extension_set = []

    for binary_tree in binary_tree_set:
        new_candidates = generate_all_tree_extensions(binary_tree, new_leaf)


        for candidate in new_candidates:
            new = True
            for prior in extension_set:
                if binary_tree_ismorphic_check(candidate, prior):
                    new = False
                    break
            if new:
                extension_set.append(candidate)

    return extension_set





def find_keys_for_tanglegram_dictionary(dictionary, tanglegram):
    """given a dictionary whose keys are left trees and entries
    are dictionaries whose keys are right trees, determine the pair of keys for the
    given tanglegram. returns back the tanglegram's trees when a new key is needed
    the first two outputs are the keys and the second two are binary indicators for
    whether the tanglegram's keys are new or not"""

    left_key = tanglegram.L
    right_key = tanglegram.R

    new_left_key = True
    new_right_key = True

    for key1, key2s in dictionary.items():
        if binary_tree_ismorphic_check(left_key, key1):

            for key2 in key2s:
                if binary_tree_ismorphic_check(right_key, key2):
                    return (key1, key2, False, False)


            return (key1, right_key, False, new_right_key)


    return (left_key, right_key, new_left_key, new_right_key)



def merge_tanglegram_dictionaries(dict1, dict2):
    """given two tanglegram dicitonaries where the first
    index is the isomorphism class of the left tree and 
    the sub-index is the right tree, merge the
    two dictionaries sub-entries and clear for isomorphism"""


    #first, prime a new dictionary
    output_dict = {}

    for left_key, right_keys in dict1.items():
        output_dict[left_key] = {}

        for right_key, entries in right_keys.items():
            output_dict[left_key][right_key] = entries.copy()



    #now merge new entries from dict2
    for dict2_left_tree, dict2_right_trees in dict2.items():

        new_left = True
        for dict1_left_tree, dict1_right_trees in dict1.items():

            if binary_tree_ismorphic_check(dict1_left_tree,dict2_left_tree):
                new_left = False



                for dict2_right_tree, dict2_tanglegrams in dict2_right_trees.items():
                    new_right = True
                    for dict1_right_tree, dict1_tanglegrams in dict1_right_trees.items():

                        if binary_tree_ismorphic_check(dict1_right_tree,dict2_right_tree):
                            new_right = False


                            for new_tanglegram in dict2_tanglegrams:
                                new = True

                                for prior_tanglegram in dict1_tanglegrams:
                                    if determine_isomorphic_assuming_trees_checked(new_tanglegram, prior_tanglegram):
                                        new = False
                                        break
                                if new:
                                    output_dict[dict1_left_tree][dict1_right_tree].append(new_tanglegram)



                    if new_right:
                        output_dict[dict1_left_tree][dict2_right_tree] = dict2_tanglegrams

        if new_left:
            output_dict[dict2_left_tree] = dict2_right_trees

    return output_dict




def generate_all_tanglegram_extensions(tanglegram, new_left_leaf, new_right_leaf):
    """given a size n tanglegram as input, generate all tanglegrams
    of size n+1 with the given tanglegram as a subtanglegram
    by extending botht trees with an extra leaf in
    all possible ways. We remove redundancies by clearing isomorphic tanglegrams"""

    possible_left_trees = generate_all_tree_extensions(tanglegram.L, new_left_leaf)
    possible_right_trees = generate_all_tree_extensions(tanglegram.R, new_right_leaf)


    new_matching = (tanglegram.sigma).copy()
    new_matching[new_left_leaf] = new_right_leaf


    #tanglegrams will be stored in a dictionary to help more-quickly determine isomorphisms
    #the index of the dictionary is the left-tree of the tanglegram
    #at each key is another dictionary storing right-trees
    #the keys here point to sets of tanglegrams
    new_tanglegrams = {}


    for left_tree in possible_left_trees:
        for right_tree in possible_right_trees:

            possible_new_tanglegram = Tanglegram(left_tree,right_tree,new_matching)

            #first, see if this is the first tanglegram by getting key info
            key_check = find_keys_for_tanglegram_dictionary(new_tanglegrams,possible_new_tanglegram)

            #if left key is new, add the new tanglegram dictionary slots
            if key_check[2]:
                new_tanglegrams[key_check[0]] = {key_check[1]:[possible_new_tanglegram]}

            #if right key is new but the left key is not, add a new key to the nested dict
            elif key_check[3]:
                (new_tanglegrams[key_check[0]])[key_check[1]] = [possible_new_tanglegram]

            #otherwise neither key is new, so we have to check for isomorphism
            else:
                new = True
                for prior in (new_tanglegrams[key_check[0]])[key_check[1]]:
                    if determine_isomorphic(possible_new_tanglegram, prior):
                        new = False
                        break

                if new:
                    ((new_tanglegrams[key_check[0]])[key_check[1]]).append(possible_new_tanglegram)

    return new_tanglegrams




def generate_tanglegram_extensions_from_set(tanglegram_set, new_left_leaf, new_right_leaf):
    """given a set of tanglegrams we extend each by the new leaf, then
    clear for isomorphisms"""
    extension_set = {}


    print_counter = 0

    for tanglegram in tanglegram_set:
        print_counter += 1
        print(print_counter)
        #this outputs a nested dictionary of tanglegrams by their left and right trees
        start_time = time.time()
        new_candidates = generate_all_tanglegram_extensions(tanglegram, new_left_leaf, new_right_leaf)
        end_time = time.time()
        print("It took ", end_time-start_time , " seconds to generate tanglegram extensions")

        start_time = time.time()
        extension_set = merge_tanglegram_dictionaries(extension_set, new_candidates)
        end_time = time.time()
        print("It took ", end_time-start_time , " seconds to merge tanglegram extensions")

    #now we want to un-pack this (for now, this is inefficiant)
    output_set = []


    for key, sub_dict in extension_set.items():
        for sub_key, items in sub_dict.items():
            for item in items:
                output_set.append(item)

    del extension_set

    return output_set
