def find_k_crossing_critical(k, n, reporting = False, produce_file = False):
    """
    finds all k-crossing critical tanglegrams with maximum size n

    if reporting = True then it will give a count of the number found at each size n' <= n

    if produce_file = path_to_directory then it will write the tanglegrams to the given text file

    k must be an integer at least 1
    """
    if not isinstance(produce_file, bool):
        file = open(produce_file, 'w')

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
            
        for T in expanders:
            print_tanglegram_to_txt(T,file)
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
        extensions = find_all_extensions(expanders,counter-1,reporting = reporting)

        expanders = []

        check_counter = 0
        for tanglegram in extensions:
            if reporting:
                check_counter += 1
                print("Checking.....", check_counter," of ",len(extensions))
            if tanglegram.crossing_number() < k:
                expanders.append(tanglegram)
            elif is_crossing_critical(tanglegram,k):
                outputs.append(tanglegram)
                print_tanglegram_to_txt(tanglegram,file)
                global_count += 1
                local_counter += 1

        if reporting:
            printing_helper_kcc(local_counter, counter, global_count, k)
        counter += 1





def printing_helper_kcc(num_found, n, total_number, k):
    print("There are ", num_found, " ", k,"-crossing critical tanglegrams of size ",n)
    print("In total we have found ", total_number, " ", k,"-crossing critical tanglegrams so far")
    print()


def print_tanglegram_to_txt(tanglegram, file):
    """
    given a tanglegram and a text file,
    adds three lines
        one for each tree as a nested bracket, and one for matching
    then leaves a space
    """

    a,b,c = tanglegram.to_bracket_format()
    
    file.write(str(a)+'\n')
    file.write(str(b)+'\n')
    file.write(str(c)+'\n')
    file.write('\n')

    return



def read_txt_to_tanglegram(filename):
    """
    given a text file formatted as would be the output of
    the print_tanglegram_to_text function,
    reads the file into a list of tanglegrams
    """

    file = open(filename, 'r')
    lines = file.readlines()
    clean_lines = [l.strip() for l in lines]
    
    tanglegrams = []

    counter = 0

    while counter < len(clean_lines)-1:
        LT = get_tree(eval(clean_lines[counter]))
        RT = get_tree(eval(lines[counter +1]))
        matching = eval(lines[counter +2])

        tanglegrams.append(Tanglegram(LT[0], LT[1], RT[0], RT[1], matching))

        counter += 4

    file.close()

    return tanglegrams


def generate_cross_responsible_tanglegrams():
    """
    outputs the two 1-crossing critical tanglegrams
    """
    K1 = Tanglegram('0123',get_tree([[0,1],[2,3]])[1],'0123',get_tree([[0,1],[2,3]])[1] ,[(0,0),(1,2),(2,1),(3,3)])
    K2 = Tanglegram('0123',get_tree([[[0,1],2],3])[1],'0123',get_tree([0,[1,[2,3]]])[1] ,[(0,0),(1,2),(2,1),(3,3)])

    return [K1, K2]
