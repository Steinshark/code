#include <iostream>
#include <math.h>
#include <string.h>
#include <climits>
using namespace std;

string int_to_bin(int);
int bin_to_int(string);
int main(){
	int number;
	cout << "Please give me a number: " << endl;
	cin >> number;
	string bin = int_to_bin(number);
	cout << bin << endl;

	int number2 = bin_to_int(bin);
	cout << number2 << endl;
}

string int_to_bin(int n){
	string binary_string = "";
	int i = 31;
	while(i > -1){
		int digit = n / pow(2,i);


		switch(digit){
			case 0:
				binary_string = binary_string + "0"; 
				i--;
			        break;	
			default:
				binary_string = binary_string + "1";
			       	n -= pow(2,i);
				i--;
				break;
		}

	}


		return binary_string;
}

int bin_to_int(string s){
	int i = 0;
	int converted = 0;
       	while(i < s.length()){
		char c = s[i];
		switch(c){
			case '0':
				i++;
				break;
			
			case '1':
				converted += pow(2,31-i);
				if(i > 16){
					cout << "char \'" << c << "\' == " << pow(2,31-i) << endl;
				}

				i++;
				break;
			default:
				cout << " bad character \'" << c << "\' has appeared" << endl;
				exit(1);
				
		}
	}
	return converted;
}
