import pandas
import requests


class project:
    def __init__(self):
        self.filepath = ""
        self.filename = ""
        self.dataframe = None
        self.verbose = input("verbose? (y/n)") == 'y'
        self.write_length = 50
        self.run_job()

    def run_job(self):
        self.open_excel()
        print(str(length := len(self.dataframe.iloc[:,0])) + " files")
        print(self.dataframe)
        input("")
        file_count = 1
        for url in self.dataframe.iloc[:,0]:
            if url[:5] == "https":
                filename = url.split('/')[-1]
                if self.verbose:
                    print("downloaded: " + self.write_filename(filename) + "\tfile " + str(file_count) + "\\" + str(length))
                open(self.filepath+filename, 'wb').write(requests.get(str(url),allow_redirects=True).content)
                file_count = file_count + 1


    def write_filename(self,string):
        file_extension = '.' + string.split('.')[1]
        file_ext_len = len(file_extension)
        if len(filename:=string[:self.write_length]) < self.write_length:
            while len(filename) < self.write_length:
                 filename = filename + " "
            return filename
        else:
            return string[:self.write_length-(file_ext_len+4)] + "... " + file_extension


    def open_excel(self):
        try:
            self.get_filepath()
            self.get_filename()
            self.dataframe = pandas.concat(pandas.read_excel(self.filename, sheet_name=None, header=None), ignore_index=True)
        except FileNotFoundError:
            print("\'" + str(self.filename) + "\' was not found")
            self.open_excel()


    def get_filepath(self,):
        self.filepath = input("save to file PATH: ")
        if not self.filepath[-1] == '\\' or not self.filepath[-1] == '/':
            self.filepath = self.filepath + '\\'

    def get_filename(self):
        self.filename = input("filename: ")

p = project()
