#include <iostream>
#include <istream>
#include <string>
using namespace std;


//------------------------------------------------------------------------------
//STRUCTS-----------------------------------------------------------------------
//------------------------------------------------------------------------------
struct midnTuple{string name; int company;};                                  //  <- holds a midn's name and co
struct roomList{midnTuple* list; int next_open_index; int current_size;};     //  <- is a list with extra steps. List of midnTuples and also keeps track of size
struct coMatcher{int company; int size; int startIndex;};                     //  <- is a tool to match a given company to the indices it will have in the list
struct coMatcherList{coMatcher* list; int size;};                             //  <- list of coMatchers
//----------------------------------------------------------------------------//


//------------------------------------------------------------------------------
//FUNCTIONS---------------------------------------------------------------------
//------------------------------------------------------------------------------
void importFromStdIn(roomList&);                                              //
void appendTo(roomList&, midnTuple);                                          //
int toNum(string);                                                            //
coMatcherList buildMatcher(roomList);                                         //
void printList(roomList);                                                     //
bool isPlacedCorrectly(int,coMatcher);                                        //
coMatcherList reOrderMatchers(roomList, coMatcherList);                       //
int findDoubleSwap(roomList,coMatcherList,int,midnTuple);                     //
//----------------------------------------------------------------------------//


//------------------------------------------------------------------------------
//RUN--------------------------------------------------------------------------
//------------------------------------------------------------------------------
int main(){                                                                   //
  string masterString = "";                                                   //  <- add swaps to this. Will print at end
  roomList midnList;                                                          //  <- this is what we are sorting. will hold structs with midnName and Co
  midnList.list = new midnTuple[1];                                           //
  midnList.next_open_index = 0;                                               //
  midnList.current_size = 1;                                                  //
  int swaps = 0;                                                              //
  importFromStdIn(midnList);                                                  //  <- fill the list from stdin
  coMatcherList matcherList = buildMatcher(midnList);                         //  <- builds the matchers for each company given the dataset
////////////////////////////////////////////////////////////////////////////////  FIND ALL MUTUAL SWAPS (places both correctly)
  for(int i = 1; i < matcherList.size; i++){                                  //  go through every matcher (they are in co order [1,2,...])
    coMatcher curMatcher = matcherList.list[i];                               //
    int startIndex = curMatcher.startIndex;                                   //    get bounds of the matcher (these will be out of order)
    int endIndex = startIndex + curMatcher.size;                              //    ''  ''
    for(int index = startIndex; index < endIndex; index++){                   //    iterate through each item within the current bounds
      midnTuple curMid = midnList.list[index];                                //
      if(isPlacedCorrectly(index,matcherList.list[curMid.company])){          //    if it is placed correctly, move on
        continue;                                                             //
      }                                                                       //
      int swapIndex = findDoubleSwap(midnList,matcherList, i,curMid);         //    if not, check to see if there exists a midn in the other company's indices that is in this company
      if(!(swapIndex==-1)){                                                   //    if the double swap does exist
        midnTuple swappingWith = midnList.list[swapIndex];                    //      do a normal swap
        masterString += midnList.list[index].name + " ";                      //
        masterString += swappingWith.name + "\n";                             //
        midnList.list[swapIndex] = midnList.list[index];                      //
        midnList.list[index] = swappingWith;                                  //
        swaps+=1;                                                             //
      }                                                                       //
    }                                                                         //
  }                                                                           //
////////////////////////////////////////////////////////////////////////////////  FIND ALL REMAINING SWAPS (places one correctly)
  for(int index = 0; index < midnList.next_open_index ;index++){              //  go through all indices in list
    midnTuple currentItem = midnList.list[index];                             //
    coMatcher currentHelper = matcherList.list[currentItem.company];          //    fetch the corresponding matcher for the current midn's company
    while(!isPlacedCorrectly(index,currentHelper)){                           //  <-we swap out of this index until we find one that belongs
      if(isPlacedCorrectly(index,currentHelper)){                             //      check if the current item belongs here
        continue;                                                             //        continue to the next index if it does
      }                                                                       //
      else{                                                                   //      otherwise:
        int indexToSwitchTo = currentHelper.startIndex;                       //        find where the current item actually belongs
        int coToSwitchTo = midnList.list[indexToSwitchTo].company;            //        find the company of the item we will switching with
        coMatcher matcherToSwitchTo = matcherList.list[coToSwitchTo];         //        find the matcher of the item we will switching with
        while(isPlacedCorrectly(indexToSwitchTo,matcherToSwitchTo)){          //        if we would be switching with something that's already where it would belong
          indexToSwitchTo += 1;                                               //          leave it and swap with the next index after it
          coToSwitchTo = midnList.list[indexToSwitchTo].company;              //          and update the new potential swap's company
          matcherToSwitchTo = matcherList.list[coToSwitchTo];                 //          and update the new potential swap's matcher
        }                                                                     //
        midnTuple swappingWith = midnList.list[indexToSwitchTo];              //        when we found where we are swapping to, build a temp
        masterString += midnList.list[index].name;                            //        add to the masterString
        masterString += " " + swappingWith.name + "\n";                       //
        midnList.list[indexToSwitchTo] = midnList.list[index];                //        and swap
        midnList.list[index] = swappingWith;                                  //        like normal
        swaps+=1;                                                             //
      }                                                                       //
      currentItem = midnList.list[index];                                     //        update the current item because we swapped
      currentHelper = matcherList.list[currentItem.company];                  //        and get its helper
    }                                                                         //  <- ^^ repeat this procedure until we swap something in that actually belongs in this index ^^
  }                                                                           //
  cout << masterString;                                                       //
  return swaps;                                                               //  <- for good measure
}                                                                             //
//----------------------------------------------------------------------------//


//------------------------------------------------------------------------------
//UTILTY FUNCITONS--------------------------------------------------------------
//------------------------------------------------------------------------------


//----------------------------importFromStdIn---------------------------------//
// DOES:    organizes the collection of names and companies from stdin        //
// RETURNS: void, we initialize the list in main and by reference             //
void importFromStdIn(roomList& bigList){                                      //
  while(cin){                                                                 //
    string raw_string;                                                        //
    midnTuple newTup;                                                         //
    string delim = " ";                                                       //
    string fetchedCompany,fetchedName;                                        //
    int i = 0;                                                                //
    getline(cin, raw_string);                                                 //
    while(raw_string[i] != ' '){                                              //  <- grab letters until the space (the company)
      fetchedCompany += raw_string[i++];                                      //
    }                                                                         //
    ++i;                                                                      //  <- skip the space
    while(i < raw_string.length()){                                           //  <- grab the remaining letters (the name)
      fetchedName += raw_string[i++];                                         //
    }                                                                         //
    if(fetchedCompany.length() < 1 || fetchedName.length() < 1){              //  <- reads from stdin a little too far idk why but this fixed it
      return;                                                                 //
    }                                                                         //
    newTup.company = toNum(fetchedCompany);                                   //  <- put it into a tuple
    newTup.name = fetchedName;                                                //
    appendTo(bigList, newTup);                                                //
  }                                                                           //
}//---------------------------------------------------------------------------//


//----------------------------appendTo----------------------------------------//
// DOES:    appends a midnTuple to a list and ammortizes insertion cost       //
// RETURNS: nothing, we passed by reference                                   //
void appendTo(roomList& midnList, midnTuple item){                            //
  int listSize = midnList.current_size;                                       //
  int next_index = midnList.next_open_index;                                  //
  roomList newMidnList;                                                       //
  if(next_index >= listSize){                                                 //  <- if its time to increase size
    newMidnList.current_size = listSize*2;                                    //  <- double the list size every time we increase
    newMidnList.list = new midnTuple[newMidnList.current_size];               //
    int i;                                                                    //
    for(i = 0;i<listSize;i++){                                                //  <- normal copy procedure
      newMidnList.list[i] = midnList.list[i];                                 //
    }                                                                         //
    newMidnList.list[i] = item;                                               //  <- add the new item, finally
    newMidnList.next_open_index = i+1;                                        //
    midnList = newMidnList;                                                   //  <- point the list we copied into to the original list
    return;                                                                   //
  }                                                                           //
  midnList.list[midnList.next_open_index++] = item;                           //  <- this is the normal add procedure if we arent increasing
  return;                                                                     //
}//---------------------------------------------------------------------------//


//--------------------------------toNum---------------------------------------//
// DOES:    takes a string representation of a number and makes an int        //
// RETURNS: an integer representation of the given string                     //
int toNum(string str){                                                        //
  if(str.length() < 2){                                                       //  <- if one digit, only return char_val - 48
    return int(str[0]-48);                                                    //
  }                                                                           //
  return int(str[0]-48)*10 + int(str[1]-48);                                  //  <- otherwise we worry about the 10's digit being multiplied
}//---------------------------------------------------------------------------//


//----------------------------buildMatcher------------------------------------//
// DOES:    makes a list of matchers that map a Company to a range of indices //
// RETURNS: the list of matchers, one for each company                        //
coMatcherList buildMatcher(roomList room_list){                               //
  coMatcherList companyMatcher;                                               //
  companyMatcher.list = new coMatcher[100];                                   //  <- assume largest case
  int lastCompany = 0;                                                        //  <- keeps track of the highest company seen so far
  for(int i = 0; i < 100;i++){                                                //
    coMatcher temp;                                                           //
    temp.size = 0;                                                            //
    companyMatcher.list[i] = temp;                                            //
  }                                                                           //  <- companyMatcher is now filled with blank matchers
  for(int i = 0; i < room_list.next_open_index;i++){                                          //  <- finds number of mids in each company
    if(companyMatcher.list[room_list.list[i].company].size == 0){             //  <- not yet initialized case
      coMatcher temp;                                                         //
      temp.company = room_list.list[i].company;                               //
      temp.size = 1;                                                          //
      companyMatcher.list[temp.company] = temp;                               //
      if(room_list.list[i].company > lastCompany){                            //  <- this is where we check what the current largest company is
        lastCompany = room_list.list[i].company;                              //
      }                                                                       //
    }                                                                         //
    else{                                                                     //  <- has already been initialized case, just increment size
      companyMatcher.list[room_list.list[i].company].size += 1;               //
    }                                                                         //
  }                                                                           //
  int sum = 0;                                                                //
  for(int i=1;i <= lastCompany;i++){                                          //  <- this loop finds the bounds by taking the sum of the
    companyMatcher.list[i].startIndex = sum;                                  //     mids in companies before it and and adding its own size:
    sum += companyMatcher.list[i].size;                                       //     (sum_up_to_this_co,sum_up_to_this_co + this_co's_size]
  }                                                                           //
  companyMatcher.size = lastCompany;
  companyMatcher = reOrderMatchers(room_list, companyMatcher);                //
  return companyMatcher;                                                      //  <- a copmany's matcher is stored in its corresponding index
}//---------------------------------------------------------------------------//     I.E. INDEX 0 IS EMPTY


//----------------------------printList---------------------------------------//
// DOES:    prints only the company number's in each of the roomList indices  //
// RETURNS: nothing, only prints                                              //
void printList(roomList list){                                                //
    for(int i=0; i < list.next_open_index;i++){                               //
      cout << list.list[i].company << ", ";                                   //
    }                                                                         //
    cout << endl;                                                             //
}//---------------------------------------------------------------------------//


//---------------------------isPlacedCorrectly--------------------------------//
// DOES:    checks to see if an index falls within the company's index range  //
// RETURNS: whether or not the index is withing the range for the company     //
bool isPlacedCorrectly(int index, coMatcher matchHelper){                      // <- the matchHelper passed is specific to the company of the index in question
  if(index >= matchHelper.startIndex){                                        //
    if(index < matchHelper.startIndex+matchHelper.size){                      //  <- checks if index lies between the start and stop index for that company
      return true;                                                            //
    }                                                                         //  *DISCLAIMER* i know this can be done in one
  }                                                                           //  line but i broke it up so it would fit
  return false;                                                               //  within the formatting blocks and look nicer:)
}//---------------------------------------------------------------------------//


//----------------------------reOrderMatchers---------------------------------//
// DOES:    place matchers so that they are optimized before attempting swaps //
// RETURNS: new coMatcherList that has been reordered                         //  <- *companies are still in order, but their indexes are different
coMatcherList reOrderMatchers(roomList midnList, coMatcherList matchers){     //
  int totalCompanies = matchers.size;                                         //
  coMatcherList newMatchers;                                                  //
  newMatchers.list = new coMatcher[totalCompanies+1];                         //
  newMatchers.size = totalCompanies;                                          //
  int coBeingPlaced = 1;                                                      //
  int curIndex = 0;                                                           //
  for(coBeingPlaced = 1; coBeingPlaced <= totalCompanies; coBeingPlaced++){       // Will place one matcher per iteration
    int bestMatchCo = 0;                                                      //                                                    //
    double bestRatio = -1.0;                                                   //
    for(int coNumber = 1; coNumber <= totalCompanies; coNumber++){            // will find which copmany this space best matches by % of its total size that it finds within it's bounds
      int numberOfMatches = 0;                                                //
      if(matchers.list[coNumber].size == 0){                                  //
        continue;                                                             //
      }                                                                       //
      for(int index = 0; index < matchers.list[coNumber].size; index++){      // find sum of matches for thsi company
        if(midnList.list[curIndex+index].company == coNumber){                //
          numberOfMatches+=1;                                                 //
        }                                                                     //
      }
      double ratio = double(numberOfMatches)/matchers.list[coNumber].size;    //
      if(ratio > bestRatio){                                                  //
        bestRatio = ratio;                                                    //
        bestMatchCo = coNumber;                                               //
      }                                                                       //
    }                                                                         //
    newMatchers.list[bestMatchCo] = matchers.list[bestMatchCo];               //  update the new list placing bestMatch where it belongs (index == company)
    newMatchers.list[bestMatchCo].size = matchers.list[bestMatchCo].size;     //
    newMatchers.list[bestMatchCo].company = bestMatchCo;                      //
    newMatchers.list[bestMatchCo].startIndex = curIndex;                      //
    matchers.list[bestMatchCo].size = 0;                                      //
    curIndex += newMatchers.list[bestMatchCo].size;                           //
  }                                                                           //
  return newMatchers;                                                         //
}//---------------------------------------------------------------------------//


//-----------------------------findDoubleSwap---------------------------------//
// DOES:    checks to see if theres 1 swap that will place 2 companies        //
// RETURNS: the index of the item to swap to or -1 if it does not exist       //
int findDoubleSwap(roomList mList,coMatcherList coList,int co, midnTuple mid){//
  coMatcher midsMatcher = coList.list[mid.company];                           //
  int startIndex = midsMatcher.startIndex;                                    //
  int endIndex = startIndex + midsMatcher.size;                               //
  for(int index = startIndex; index < endIndex; index++){                     //  <- look through all midn in this company's index space
    if(mList.list[index].company == co){                                      //
      return index;                                                           //
    }                                                                         //
  }                                                                           //
  return -1;                                                                  //
}//---------------------------------------------------------------------------//
