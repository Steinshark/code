#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <cmath>
#include <locale>
#include <algorithm>


using namespace std;
struct runReturn{int mispeleability;vector<string> pairs;};

runReturn run(vector<string>,string,map<string,int>);
bool isSimilar(string,string);

int main(){


  //VAR INIT
  fstream file;
  time_t start, end;
  string filename, rawName;
  int countUpTo = 0, it=0;
  map<int,vector<string>> nameList_byLength;
  map<string,int> mispeleability;
  map<string,int> counts;
  map<string,int> sizes;
  locale loc;


  //IO
  cout << "FILE: ";
  cin >> filename;
  cout << "\nCOUNT: ";
  cin >> countUpTo;
  //CODE
  file.open(filename);

  // INITIAL READ and COUNT LOOP (O(n)
  while(file >> rawName){
    int length = rawName.length();
    string builtName = tolower(rawName[0],loc) + rawName.substr(1,length-1);
    if(counts.count(builtName)){
      counts[builtName] += 1;
    }

    else{
      nameList_byLength[length].push_back(builtName);
      counts[builtName] = 1;
      sizes[builtName] = length;
    }
  }

  for(auto item : counts){
    string root = item.first;
    int count = root.length();
    vector<string> matches;
    for(auto name : nameList_byLength[count-1]){
      if(isSimilar(root,name)){
        matches.push_back(name);
      }
    }
    for(auto name : nameList_byLength[count]){
      if(isSimilar(root,name)){
        matches.push_back(name);
      }
    }
    for(auto name : nameList_byLength[count+1]){
      if(isSimilar(root,name)){
        matches.push_back(name);
      }
    }
    double sum = 0;
    int rootCount = counts[root];
    for(auto name : matches){
      if(counts[name] < rootCount){
        sum += counts[name];
      }
    }
    mispeleability[root] = round(100*(sum/counts[root]));
  }

  //GET TOP 10
  vector<string> topTen;
  for(int i = 0; i < countUpTo; i++){
    int max = 0;
    string max_item;
    for(auto item : mispeleability){
      if(item.second > max && !(find(topTen.begin(), topTen.end(),item.first) != topTen.end())){
        max = item.second;
        max_item = item.first;
      }
    }
    topTen.insert(topTen.end(),max_item);
  }
  for(string name : topTen){
    cout << name << " " << mispeleability[name] << endl;
  }
}
bool isSimilar(string name, string name2){
  int n1Len = name.length();
  int n2Len = name2.length();

  if(n2Len > n1Len){
    string temp = name2;
    name2 = name;
    name = temp;
    int temp2 = n1Len;
    n1Len = n2Len;
    n2Len = temp2;
  }

  if(n1Len == n2Len){
    int fails = 0;
    for(int i = 0; i < n2Len;i++){
      if(!(name[i] == name2[i])){
        fails += 1;
        if(fails > 1){
          return false;
        }
      }
    }
    return true;
  }
  else{
    if(name.substr(0,n1Len-1) == name2){
      return true;
    }
    else{
    }
    if(name.substr(1,n1Len-1) == name2){
      return true;
    }
    int first_break = 0;
    for(int i = 0; i < n1Len;i++){
      char letter = name[i];
      if(!(letter == name2[i])){
        first_break = i;
        break;
      }
    }
    first_break += 1;
    for(int i = first_break; i < n1Len; i++){
      char letter = name[i];
      if(!(letter == name2[i-1])){
        return false;
      }
    }
    return true;
  }
  return false;
}
