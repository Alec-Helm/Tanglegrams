# Tanglegrams

This repository stores all code used for calculations in the paper: 

All code is written in Sage, and was written for v10.4


## How to use the code
All of the functions contained here are based on the the tanglegram class and functions provided [here](https://github.com/AMS-MRC-tanglegrams/tanglegrams).

The file **tanglegram_functions.sage** primarily exists for two purposes.

(1) The *subtanglegram* function allows one to produce subtanglegrams given a tanglegram and a set of edges. 

(2) The *find_all_extensions* function intakes a set of tanglegrams all of the same size, and outputs all tanglegrams of size one greater
which contains one of the tanglegrams from the list as an induced subtanglegram

The file **crossing_critical_functions.sage** contains the function *find_k_crossing_critical(k, n)*, which produces all k-crossing critical tanglegrams of size at most n. The function is not particularly optimized, and was only made to be used for *k=2* and *n=8*. 

The file **two_crossing_critical_tanglegrams.tex** contains a full list of all 2-crossing critical tanglegrams. Each tanglegram takes 3 lines. The first is the nested bracket format for the left tree, then for the right tree, then the tuples of the matching. Tanglegrams have one line of spacing between them. Tanglegrams are listed in increasing size order; ie, all size 5, then size 6, and so on. As shown in our paper, there are 2 at size 5, 155 at size 6, 331 at size 7, and ??? at size 8.
