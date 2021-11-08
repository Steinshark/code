if (files := [open('mod'+str(i)+'.txt', 'w') for i in [0,1,2]]) and (input := [int(line) for line in open('numbers.txt','r')]): [files[number%3].write(str(number)+'\n') for number in input]
