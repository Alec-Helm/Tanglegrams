def find_k_crossing_critical(k, n, reporting = False):
    """
    finds all k-crossing critical tanglegrams with maximum size n

    if reporting = True then it will give a count of the number found at each size n' <= n

    k must be an integer at least 1
    """

    if reporting:
        printing_helper_kcc(0, 1, 0, k)
        printing_helper_kcc(0, 2, 0, k)
        printing_helper_kcc(0, 3, 0, k)

    expanders = generate_cross_responsible_tanglegrams()
    counter = 4
    
    if k == 1:
        printing_helper_kcc(2, 4, 2, k)
        while counter < n:
            counter += 1
            printing_helper_kcc(0, counter, 2, k)
        return expanders

    
    outputs = []
    counter += 1
    global_count = 0
    
    while counter <= n:
        #the expanders are tanglegrams of size counter-1 which have crossing number < k
        #we extend all by adding a single new edge in all possible ways
        #each new tanglegram we find is either still too low crossing number, in which case we add it to the new expanders
        #it could be k-crossing-critical, in which case we add it to the output list and up the relavant counters
        #or neither, in which case we ignore it
        local_counter = 0
        extensions = find_all_extensions(expanders,counter-1)

        expanders = []

        lopunny = 0
        for tanglegram in extensions:
            lopunny += 1
            print("Checking.....", lopunny," of ",len(extensions))
            if tanglegram.crossing_number() < k:
                expanders.append(tanglegram)
            elif is_crossing_critical(tanglegram,k):
                outputs.append(tanglegram)
                global_count += 1
                local_counter += 1

        if reporting:
            printing_helper_kcc(local_counter, counter, global_count, k)
        counter += 1





def printing_helper_kcc(num_found, n, total_number, k):
    print("There are ", num_found, " ", k,"-crossing critical tanglegrams of size ",n)
    print("In total we have found ", total_number, " ", k,"-crossing critical tanglegrams so far")
    print()





def generate_cross_responsible_tanglegrams():
    """
    outputs the two 1-crossing critical tanglegrams
    """
    K1 = Tanglegram('0123',get_tree([[0,1],[2,3]])[1],'0123',get_tree([[0,1],[2,3]])[1] ,[(0,0),(1,2),(2,1),(3,3)])
    K2 = Tanglegram('0123',get_tree([[[0,1],2],3])[1],'0123',get_tree([0,[1,[2,3]]])[1] ,[(0,0),(1,2),(2,1),(3,3)])

    return [K1, K2]
