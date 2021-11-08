import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import string
import re
import os
import tkinter
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askdirectory
from Utils import Utils
import threading
import tkinter.scrolledtext as st
class Chickles:


    ########################################################################################################
    ########################################################################################################
    ########################################################################################################
    def __init__(self):
    ########################################################################################################
        self.INPUT_FILE_PATH = os.getcwd() + "\\"
        self.INPUT_FILE_NAME = None
        self.INPUT_FULL_PATH = None
        self.build_job = None
        self.OUTPUT_FILE_PATH = os.getcwd() + "\\"
        self.OUTPUT_FILE_NAME = None
        self.OUTPUT_FULL_PATH = None
        self.thread_running = False
        self.WEBSITE = r"https://cis.scc.virginia.gov"
        self.requestURL = "https://cis.scc.virginia.gov/EntitySearch/Index"
        self.CSV_HEADER = "ID#,NAME,ADDRESS,CITY,STATE,ZIP,TITLE,HOANAME,TYPE,HOASTATE,HOAZIP,COUNTY,ENTERED,ASOF\n"
        self.window = self.make_gui()


    ########################################################################################################
    ########################################################################################################
    ########################################################################################################
    def import_HOAs(self):
    ########################################################################################################
        import csv
        csv_reader = csv.reader(open(self.INPUT_FULL_PATH), delimiter=",")

        HOA_plain_ids = list()
        HOA_IDs = list()
        for datapoint in csv_reader:
            if datapoint[1] == '':
                break
            #                           ID         HOANAME       TYPE            STATE       HOAZIP          HOACOUNTY
            small_list = [datapoint[0], datapoint[7], datapoint[8], datapoint[9], datapoint[10], datapoint[11]]
            if not datapoint[0] in HOA_plain_ids:
                HOA_plain_ids.append(datapoint[0])
                HOA_IDs.append(small_list)
        return HOA_IDs
    ########################################################################################################
    ########################################################################################################
    ########################################################################################################
    def tryOtherOG(self):
    ########################################################################################################
    #   setup csv file we will write to
        self.output_writer.insert(tkinter.END, ("Starting Job\n"))
        self.output_writer.yview(tkinter.END)
        file = open(self.OUTPUT_FULL_PATH, 'w')
        file.write(self.CSV_HEADER)
        file.close()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        (driver := webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)).get(self.requestURL)  #
        HOAs_to_process = len(self.HOA_IDs) - 1
        current_HOA = 1
        for data in self.HOA_IDs[1:]:
            if not self.thread_running:
                self.output_writer.insert(tkinter.END, ("Stopped execution\n")[:self.main_frame.winfo_width()])
                self.output_writer.yview(tkinter.END)
                return
            try:
                time_start = time.time()
                #   get ID and name of HOA from 6-tuple
                ID, HOANAME, TYPE, HOASTATE, HOAZIP, HOACOUNTY = data
                ##          setup web API           #################################################
                driver.get(self.requestURL)
                driver.find_element_by_id("BusinessSearch_Index_txtBusinessID").send_keys(ID)
                driver.find_element_by_id("btnSearch").send_keys(Keys.RETURN)
                driver.find_element_by_class_name("loading").send_keys(Keys.RETURN)
                #   skims out the table containing board member information.
                #   *is still raw HTML*
                cut = re.split("bgwhite|bgrowalt", driver.page_source)
                cut[len(cut)-1] = cut[len(cut)-1].split("</script")[0]
                finalcut = cut[1:]
                #GET AS_OF
                driver.find_elements_by_name("btnSearch")[0].send_keys(Keys.RETURN)
                cut = driver.page_source.split("bgwhite")[1]
                date = cut[6:16]
                #   parse html rows for [Position, Name, Address, Date] to write to csv
                parsed_row_data = list()
                i = 0
                # write data
                self.output_writer.insert(tkinter.END, "Building data " + str(current_HOA) + "/" + str(HOAs_to_process) + " \"" + str(HOANAME.title()) + '\"\n')
                for line in finalcut:
                    file = open(self.OUTPUT_FULL_PATH, 'a')
                    file.write("\'" + str(ID) + ",")

                    #through each data point
                    self.output_writer.insert(tkinter.END, ("\tWrote Member\n")[:self.main_frame.winfo_width()])
                    self.output_writer.yview(tkinter.END)
                    for item in Utils.parseLine(line):
                        file.write(Utils.build_commas(item) + ",")
                    file.write(Utils.build_commas(string.capwords(str(HOANAME))) + ',' + Utils.scrub_type(str(TYPE).title()) + ',' + str(HOASTATE).upper() + ',' + str(HOAZIP).title() + ',' + str(HOACOUNTY).title() + ',1/12/21,' + str(date) + "\n")

                file.close()

            except ElementNotInteractableException:
                self.output_writer.insert(tkinter.END, "Bad data grab, possibly a bad CSV value\nalso check internet")
                self.output_writer.yview(tkinter.END)
            current_HOA = current_HOA + 1
        self.output_writer.insert(tkinter.END, "Finished building dataset!\n")
        self.thread_running = False
        self.output_writer.yview(tkinter.END)

    def execute(self):
        self.INPUT_FILE_NAME = self.file_in_input.get()
        self.OUTPUT_FILE_NAME = self.file_out_input.get()
        if self.INPUT_FILE_NAME == '':
            Utils.write(self.output_writer, "No file specified\n")
            return

        if self.OUTPUT_FILE_NAME == '':
            Utils.write(self.output_writer, "Save file as what?\n")
            return
        try:
            self.OUTPUT_FULL_PATH = self.OUTPUT_FILE_PATH + self.OUTPUT_FILE_NAME
            Utils.write(self.output_writer, "Writing " + str(self.OUTPUT_FULL_PATH) + "\n")

            self.HOA_IDs = self.import_HOAs()
            self.build_job = threading.Thread(target=self.tryOtherOG)
            self.thread_running = True
            self.build_job.start()
        except FileNotFoundError:
            err_message = "Filepath \'" + str(self.INPUT_FILE_PATH) + str(self.INPUT_FILE_NAME) + "\' is not valid"
            Utils.write(self.output_writer, err_message)

            pass
        return

    def cancel_execution(self):
        if self.build_job == None:
            Utils.write(self.output_writer, "No Thread Running\n")
            return
        if self.build_job.is_alive():
            self.thread_running = False
        else:
            Utils.write(self.output_writer, "There was an error killing thread\n")
            return



    def get_file(self):
            file = askopenfile(filetypes=(("csv files","*.csv"),("All files","*.*")))
            err_message = '\'' + str(file.name).replace('/', '\\') + "\' selected\n"
            Utils.write(self.output_writer, err_message)
            print(file)

            self.file_in_input.delete(0, tkinter.END)
            self.file_in_input.insert(0, Utils.get_file_name(file.name))
            self.INPUT_FULL_PATH = file.name

    def get_directory(self):
            directory = askdirectory()
            self.OUTPUT_FILE_PATH = directory + '/'
            err_message = 'Saving to \'' + str(self.OUTPUT_FILE_PATH) + "\'\n"
            Utils.write(self.output_writer, err_message)


    def make_gui(self):
        self.window = tkinter.Tk("Chickles")
        self.window.geometry("800x500")
        self.window.title("Web Scraper Utility 0.1")

        #build menu
        self.options_menu = tkinter.Menu(self.window, tearoff=0)
        self.options_menu.add_command(label="Exit", command=self.window.quit)
        self.options_menu.add_command(label="Input File", command=self.get_file)
        self.options_menu.add_command(label="Save Directory", command=self.get_directory)
        #build frames
        self.input_frame = tkinter.Frame(height=30)
        self.main_frame = tkinter.Frame(height=30)
        self.run_frame = tkinter.Frame(height=30)
        self.out_frame = tkinter.Frame(height=100)

        #input file
        self.file_in_title = tkinter.Label(master=self.input_frame, text="Input File", width=10, height=2)
        self.file_in_input = tkinter.Entry(master=self.input_frame, width=15)
        self.file_in_button = tkinter.Button(master=self.input_frame, text="Select File", command=self.get_file)
        #output file
        self.file_out_title = tkinter.Label(master=self.main_frame, text="Output File", width=10, height=2)
        self.file_out_input = tkinter.Entry(master=self.main_frame, width=15)
        self.output_button = tkinter.Button(master=self.main_frame, text="Save To Folder", command=self.get_directory)
        #execution
        self.submit_button = tkinter.Button(master=self.run_frame, text="Run Job", command=self.execute)
        self.cancel_button = tkinter.Button(master=self.run_frame, text="Canel Job", command=self.cancel_execution)

        #pack input
        self.file_in_title.pack(side=tkinter.LEFT)
        self.file_in_input.pack(side=tkinter.LEFT)
        self.file_in_button.pack(side=tkinter.LEFT)

        #pack output
        self.file_out_title.pack(side=tkinter.LEFT)
        self.file_out_input.pack(side=tkinter.LEFT)
        self.output_button.pack(side=tkinter.LEFT)
        #pack execution
        self.submit_button.pack(side=tkinter.LEFT)
        self.cancel_button.pack(side=tkinter.LEFT)

        #pack frames
        self.input_frame.pack(fill=tkinter.X)
        self.main_frame.pack(fill=tkinter.X)
        self.run_frame.pack(fill=tkinter.X, padx=(20, 10))

        #job run
        self.window.update()
        self.output_writer = st.ScrolledText(master=self.out_frame, width=self.main_frame.winfo_width(), height=15)
        self.output_writer.pack(side=tkinter.LEFT)



        self.out_frame.pack(fill=tkinter.X, padx=(20,10))

        message = '\'' + str(self.INPUT_FILE_PATH) + "\' being used as default save path\n"
        Utils.write(self.output_writer, message)
        self.window.mainloop()
########################################################################################################
########################################################################################################
########################################################################################################
#RUN
########################################################################################################

c = Chickles()
