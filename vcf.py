import csv

def begin():
    filename = str(input("filename: "))
    print(filename)
    file_in = open(filename)
    reader = csv.DictReader(file_in)
    
    name_number = {}
    print(reader.fieldnames)
    for row in reader:
        for name,number in [('1/C','1/C NUM'),('2/C','2/C NUM'),('3/C','3/C NUM'),('4/C','4/C NUM')]:
            if not row[name] == 'END':
                phone = row[number]
                number = '(' + str(phone[:3]) + ') ' + str(phone[3:6]) + '-' + str(phone[6:])
                name_number[row[name]] = number
    
    file_out = open("30.vcf",'w')
    for name in name_number.keys():
        file_out.write("BEGIN:VCARD\nVERSION:3.0\n")
        file_out.write('N:' + str(name) + '\n')
        file_out.write('FN:' + str(name) + '\n')
        file_out.write('TEL;CELL;VOICE:' + str(name_number[name]) + '\n')
        file_out.write('REV:20210914T033923Z\n')
        file_out.write('END:VCARD\n')

    file_out.close()


begin()

