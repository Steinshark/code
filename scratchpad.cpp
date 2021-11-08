#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

int main(){
	ifstream file;
	file.open("names.txt");
	vector<string> names;
	string name;

	while(file << name){
		names.push_back(name);
	}
}
