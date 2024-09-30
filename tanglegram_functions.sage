def subtanglegram(tanglegram, edge_set):
    """
    returns a new tanglegram which is the subtanglegram
    of the given tanglegram induced on the given edges

    edge_set should be formatted as list of matchings
    just as when defining a new tanglegram

    for compatability with prior tanglegram functions,
    the leaves are re-labeled to be integers 0,...,k-1

    edges in edge_set which do not belong to tanglegram are ignored
    """
    original_left_tree, original_right_tree, original_matching = tanglegram.to_bracket_format()

    new_left_tree_nested = induced_subtree(original_left_tree, [l for l,r in edge_set])
    new_right_tree_nested = induced_subtree(original_right_tree, [r for l,r in edge_set])

    new_left_tree_nested_corrected = re_index_tree(new_left_tree_nested, list(range(len(write_down(new_left_tree_nested)))))
    new_right_tree_nested_corrected = re_index_tree(new_right_tree_nested, list(range(len(write_down(new_right_tree_nested)))))

    new_left_tree = get_tree(new_left_tree_nested_corrected[0])
    new_right_tree = get_tree(new_right_tree_nested_corrected[0])

    compressed_matching = [x for x in edge_set if x in original_matching]

    new_matching = re_index_matching(compressed_matching, new_left_tree_nested_corrected[1], new_right_tree_nested_corrected[1])

    return Tanglegram(new_left_tree[0], new_left_tree[1], new_right_tree[0], new_right_tree[1], new_matching)




def induced_subtree(tree, leaf_set):
    """
    given a rooted binary tree in nested bracket format
    and s subset of its leaves, return the induced subtree
    on the given leafset

    subtree is returned as nested list
    
    leaves in leaf_set which do not belong to tree are ignored
    """

    if isinstance(tree, list) == False:
        if tree in leaf_set:
            return tree
        return 

    upper_tree = induced_subtree(tree[0], leaf_set)
    lower_tree = induced_subtree(tree[1], leaf_set)
    next_tree = [upper_tree, lower_tree]

    if None not in next_tree:
        return [upper_tree, lower_tree]
    return [subtree for subtree in [upper_tree, lower_tree] if subtree is not None][0]




def re_index_tree(tree, labels):
    """
    given a binary tree in nested list format,
    returns an isomorphic tree with leaves labels
    from the list of labels as well as the permutation 
    performed as a list of tuples
    """
    permutation = []

    if isinstance(tree,list) == False:
        permutation = [(tree, labels[0])]
        return (labels[0], permutation)

    if isinstance(tree[0],list) == True:
        upper_len = len(write_down(tree[0]))
    else:
        upper_len = 1
    if isinstance(tree[1],list) == True:
        lower_len = -len(write_down(tree[1]))
    else:
        lower_len = -1
    upper_tree, upper_tree_permutation = re_index_tree(tree[0],labels[:upper_len])
    lower_tree, lower_tree_permutation = re_index_tree(tree[1],labels[lower_len:])

    return ([upper_tree,lower_tree], upper_tree_permutation+lower_tree_permutation)



def re_index_matching(matching, left_permutations, right_permutations):
    """
    we are given a list of pairs of leaves
    and a permutation on the left (initial)
    and right (terminal) leaves. We output
    the new matching with the permutation performed
    """

    new_matching = []

    for m in matching:
        new_m = ([x[1] for x in left_permutations if x[0] == m[0]][0], [y[1] for y in right_permutations if y[0] == m[1]][0])
        new_matching.append(new_m)

    return new_matching



def is_crossing_critical(tanglegram, k):
    """
    determines if the tanglegram is
    k-crossing critical by first determining
    if tcr is at least k, then checking the 
    tangle crossing number of all size n-1
    subtanglegrams
    """


    if tanglegram.crossing_number() < k:
        return False

    for edge in tanglegram.matching:
        subtanglegram_edges = [m for m in tanglegram.matching if m != edge]

        sub = subtanglegram(tanglegram, subtanglegram_edges)
        if sub.crossing_number() >= k:
            return False
    return True



def find_all_extensions(tanglegram_set,n):
    """
    given a set of tanglegrams all of the same size n,
    determines all tanglegrams of size n+1 with one of the
    given tanglegrams as a subtanglegram
    """

    new_tanglegrams = []
    count = 0
    for tanglegram in tanglegram_set:
        count +=1
        print("Extending.....", count," of ",len(tanglegram_set))
        candidates = extend_tanglegram(tanglegram,n)
        new_tanglegrams = merge_tanglegram_lists(new_tanglegrams, candidates)


    return new_tanglegrams



def extend_tanglegram(tanglegram,n):
    """
    given a tanglegrams of size n-1,
    determines all tanglegrams of size n
    the tanglegram as a subtanglegram

    the new matching edge is (n,n)
    """
    left_tree, right_tree, matching = tanglegram.to_bracket_format()

    new_left_trees = extend_tree(left_tree, n)
    new_right_trees = extend_tree(right_tree, n)
    matching.append((n,n))

    new_tanglegrams_candidates = []

    for L in new_left_trees:
        for R in new_right_trees:

            #due to an oddity in the original tanglegram function, I believe that the leaf labels need to be consistent with a leaf ordering in a layout
            #as such, we re-order the leaves with 0,...,n-1
            L_corrected, left_perm = re_index_tree(L, list(range(n+1)))
            R_corrected, right_perm = re_index_tree(R, list(range(n+1)))
            matching_corrected = re_index_matching(matching, left_perm, right_perm)
            
            LT = get_tree(L_corrected)
            RT = get_tree(R_corrected)

           

            new_tanglegrams_candidates = merge_tanglegram_lists(new_tanglegrams_candidates, [Tanglegram(LT[0], LT[1], RT[0], RT[1], matching_corrected)])
            #new_tanglegrams_candidates.append(Tanglegram(LT[0], LT[1], RT[0], RT[1], matching))
    
    return new_tanglegrams_candidates





def extend_tree(tree, n):
    """
    given a tree of size n-1,
    determines all trees of size n
    the tree as an induced subtree

    the new leaf gets the label 'n'

    tree is given as a nested list
    """
    new_trees = []

    #first let the new leaf by a child of the root
    new_trees.append([tree, n])

    #then recur through the subtrees
    if isinstance(tree,list) == True:
        upper_tree = tree[0]
        lower_tree = tree[1]
        
        new_upper_trees = extend_tree(upper_tree, n)
        new_lower_trees = extend_tree(lower_tree, n)

        for A in new_upper_trees:
            new_trees.append([A,lower_tree])
        for B in new_lower_trees:
            new_trees.append([upper_tree,B])
    return new_trees





def merge_tanglegram_lists(list_A, list_B):
    """
    given two lists of tanglegrams, we add
    all elements of B to list A which are
    not ismorphic to any element of A,
    and for multiple ismorphic copies of the 
    same tanglegram in B we only add one copy to A
    """

    new_list = copy(list_A)

    for candidate in list_B:
        new = True

        for tanglegram in new_list:
            if candidate.is_isomorphic(tanglegram):
                new = False
                break

        if new == True:
            new_list.append(candidate)

    return new_list

