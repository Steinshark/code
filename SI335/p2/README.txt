EVERETT STENBERG M226252

REFERENCES----------------------------------------------------------------------
    brannon purvis: big concepts like how long each function call takes

    stack-overflow: lots of c++ help, including
                        - vector iteration
                        - map iteration
                        - vector and map insert and delete
                        - vector and map search

HOW IT WORKS--------------------------------------------------------------------
    1) read in a list of names and:
            creates a map of individual ones we find
            finds the length of a name
            keeps a map1 of (int,vector<string>) of (l, names of a length l)
            keeps a map2 of (string,vector<string>) (name, similar_names)

    2) iterate through all distinct names:
            search through all names with deltasize == 1
            if its similar, add each name to each other's map2
            compute the name's mispeleability and record in a master vector
            delete name from map1, we found all pairings with that name already

    3) brute force search for top 10 mispeleabilities in master vector

HOW I BECAME THE GENIUS THAT I AM NOW AFTER HAVING DONE THIS PROJECT------------
    - i initially tried brute force, using a call from part 1 on each name
    - this was terrible
    - i then realized i only had to search distinct names
    - i then realized a bunch of optimizations, including:
        i can pre-compute each name's length only once
        i can pre-compute each name's count in the file
        i can track all similar name pairs and delete the one i just checked
        i can split my issimilar on a case by case basis to do less work because
          i already know the length of each string based on my program's design
        i can try to use only constant time vector algorithms

RUNTIME-------------------------------------------------------------------------
    - initial file read is O(nm), as finding the length of each name (m) times
        number of names (n) is the dominating function
    - computing mispeleability is O(m(k^2)), as worst case scenario all names are
        equal length and the check for similarity is proportional to m
    - top 10 search is O(k*count), though count should be small enough so that
        it does not seriously affect run time

    combined, we are now at O(nm + m(k^2) + k)
    this is dominated by m(k^2)
    thus we have O(m(k^2)) 
