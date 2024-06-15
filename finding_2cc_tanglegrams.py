from tanglegram_class import *
import time


#generate tanglegrams of size 4
Simplest_Tree = create_binary_tree('1')
Simplest_Matching = {'1':'1'}

Simplest_Tanglegram = Tanglegram(Simplest_Tree, Simplest_Tree, Simplest_Matching)
Current_Tanglegrams = [Simplest_Tanglegram]
Current_Trees = [Simplest_Tree]


for i in [2,3,4]:
    Current_Tanglegrams = generate_tanglegram_extensions_from_set(Current_Tanglegrams, str(i), str(i))



#tidy up
del Simplest_Tree, Simplest_Matching, Simplest_Tanglegram


#gather the 1-cc tanglegrams
current_Tanglegrams = []
for t in Current_Tanglegrams:
    if t.get_crossing_number() == 1:
        current_Tanglegrams.append(t)



#count 1-cc
print("There are " , len(current_Tanglegrams), " distinct crossing-critical tanglegrams")
print()


two_crossing_critical_tanglegrams = []


for i in [5,6,7]:
    print("Beginning to Count Size", str(i))
    print("---------------------------------------------------------------------------")
    check_Tanglegrams = generate_tanglegram_extensions_from_set(current_Tanglegrams, str(i), str(i))
    print("---------------------------------------------------------------------------")


    print("There are " , len(check_Tanglegrams), " distinct tanglegrams of size ", str(i), " to check")

    next_Tanglegrams = []

    print_counter = 0
    for tanglegram in check_Tanglegrams:
        print_counter += 1
        print(print_counter)

        if tanglegram.get_crossing_number() > 1:
            if tanglegram.is_crossing_critical(2):
                two_crossing_critical_tanglegrams.append(tanglegram)
        else:
            next_Tanglegrams.append(tanglegram)

    print("---------------------------------------------------------------------------")
    print("We found ", len(two_crossing_critical_tanglegrams), " two-crossing-critical tanglegrams so far.")


    current_Tanglegrams = next_Tanglegrams
    print("There are ", len(current_Tanglegrams), " tanglegrams of size ", str(i), " which need to be extended")
    print()
    time.sleep(30) 