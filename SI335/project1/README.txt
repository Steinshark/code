EVERETT STENBERG
m226252



REFERENCES
#########################################################################################################
- I discussed my final method with Brannon Purvis. Both of us had finalized how we would do it, this
  did not impact my project at all and, as far as I know, it did not impact his.


- This was my first time using C++ since IC210. Thus, I referenced a lot of dumb articles:
      - http://www.cplusplus.com/doc/tutorial/structures/           because I forgot how to do structs
      - https://www.w3schools.com/cpp/cpp_strings_length.asp        length of strings
      - http://www.cplusplus.com/reference/string/string/getline/   forgot how to read from input



HOW IT WORKS
#########################################################################################################
- TLDR: Use a list, figure out indices where each company will best fall in between, and iterate through
  the list twice. First to find mutual swaps, second to find remaining swaps.

  1) Read StdInput into a list of "midnTuple" structs holding a Co and a Name.
  2) Go through the unsorted list and determine how many mids are in each company
  3) For each unique company we identify, build a "matcher" struct that counts mids in the company.
  4) Build a set of bounds that each company will eventually fall into once sorted.
  5) Rearrange the bounds such that the most midn in that company already fall inside them.
  6) Swapping Alg:
        Iterate through each company matcher:
            iterate through each matcher's indices:
                check if the midn in the list at this index belongs here
                if not, find where they actually belong and iterate through THAT company's indices for a mid in the current company
                if we find one, we perform a mutual swap (we place 2 mids correctly)
                else we move on
        Iterate through the midnList:
            if the mid at 0 is in the right spot, move on to the next index
              otherwise, find the first open index for this mid's company using their company's matcher
              swap this mid into that spot, and figure out who's now at the current index
              if this person also does not belong here, swap them into the first open index of their company
              repeat until the mid at index 0 actually belongs in index 0
            move on to the next index



RUNTIME ANALYSIS
#########################################################################################################
Breakdown by portion
  - Grab Input:
        all-cases:      Theta(n)        <- reads n inputs
  - Build matchers:
        all-cases:      Theta(n)        <- must search through full list to count numbers of mids in each copmany
  - Sort matchers:
        all-cases:      Theta(k*n)      <- loop of size k, with nested loop of size k, with nested loop size n/k
  - Find mutual swaps:
        worst-case:     Theta(n^2/k)    <- loops of size k, with nested loop of size n/k, with nested loop of size n/k
        average-case:   O(n^2/k)        <- same loop as above, but sometimes will run findDoubleSwap on first index check
        best-case:      Theta(n)        <- best case is that every mid is placed correctly
  - Find single swaps:
        all-cases:      Theta(n)        <- when completely out of order, each iteration places one midn every time. When in order, we still have to check through the full list.

Total
  - Full run:
        worst-case:     Theta(n^2/k)    <- will be strictly bounded by the dominant worst case scenario from above
        average-case:   O(n^2/k)        <- will be upper bounded by worst-case but will not be lower bounded
        best-case:      Theta(n)        <- when list is completely sorted



SWAP ANALYSIS
#########################################################################################################
Breakdown by portion
  - Find mutual swaps:
        worst-case:     Theta(n)                                < every mid is out of order and no swaps are mutual
        average-case:   Theta(n^2/k^3 mutual swaps + n-2*(n^2/k^3) normal swaps - n/k already matched
        best-case:      Theta(1)                                <- the entire list is already sorted
  - Remaining swaps:
        all-cases:      Theta(n)                                <- always proportional to n
