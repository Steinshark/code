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
from Utils import Utils
import re
import csv
import matplotlib.pyplot as plt
import numpy
from selenium.common.exceptions import WebDriverException

class VAScraper:
    def __init__(self):
        self.URL = "https://mblsportal.sos.state.mn.us"
        self.URL_FIRST = "https://cis.scc.virginia.gov/EntitySearch/BusinessInformation?businessId="
        self.URL_SECOND = "&source=FromEntityResult&isSeries=False"
        self.BusinessGrabs = list()
        self.items_grabbed = 0
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.write_file = r"E:\DataSets\full_VA_list_TEST.csv"
        self.csv_header = "entity_name,entity_ID,entity_type,entity_status,formation_date,reason_for_status," +\
                          "va_qualification_date,status_date,industry_code,duration_period,jurisdiction,annual_report_due_date,registration_fee_due_date,charter_fee,email,contact,"+\
                          "regstered_agent_type,locality,registered_agent_qual,regist   ered_agent_name,registered_agent_address,"+\
                          "office_addr,"+\
                          "member_1_name,foreign,member_1_addr,member_1_city,member_1_state,member_5_zip,member_5_country,member_1_title,"+\
                          "member_2_name,foreign,member_2_addr,member_2_city,member_2_state,member_5_zip,member_5_country,member_2_title,"+\
                          "member_3_name,foreign,member_3_addr,member_3_city,member_3_state,member_5_zip,member_5_country,member_3_title,"+\
                          "member_4_name,foreign,member_4_addr,member_4_city,member_4_state,member_5_zip,member_5_country,member_4_title,"+\
                          "member_5_name,foreign,member_5_addr,member_5_city,member_5_state,member_5_zip,member_5_country,member_5_title,shares,last_updated\n"
                                                                    #10
        self.infoBase = [['','','','','','','','','','','','','','','',''],\
                    ['','','','',''],\
                    [''],\
                    #30
                    ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],\
                    [''],\
                    ['']\
                    ]

        self.datapoints = list()
        self.search_iter = 1000
        self.scrape_into_csv()


    def scrape_into_csv(self):
        try:
            file2 = open(self.write_file, "r")
            csv_reader = csv.reader(file2)
            start_row = sum(1 for row in csv_reader) + 1000000
            file2.close()
        except FileNotFoundError:
            start_row=35301
        print("starting on " + str(start_row))
        #, "--headless"
        # DRIVER
        #"headless",
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=Utils.build_options(["--log-level=3","headless","user-agent="+self.user_agent]))
        # WRITE CSV HEADER
        #NOT APPENDING
        #(file := open(self.write_file, "w")).write(self.csv_header)
        #APPENDING

        # SEARCH THE DATA
        #range(1, 1864500)
        for search_item in range(start_row, 1864500):
            time1 = time.time()
            if (search_item%self.search_iter) == 0:
                VAScraper.build_graph(self.datapoints, int(search_item/self.search_iter))
                self.datapoints = list()
                print("resetting driver")
                driver = webdriver.Chrome(ChromeDriverManager().install(),options=Utils.build_options(["--log-level=3","headless","user-agent="+self.user_agent]))
            web_lookup_time_1 = time.time()
            try:
                driver.get(self.URL_FIRST + str(search_item) + self.URL_SECOND)
            except WebDriverException:
                driver = self.retry_connection(driver, self.URL_FIRST + str(search_item) + self.URL_SECOND)
            web_lookup_time = time.time() - web_lookup_time_1


            computation_time_1 = time.time()
            ### BUILD THE CSV LINE
            types_pre_list = list()
            try:
                types_pre_list = driver.page_source.split("col-md-12 section-title")[1:]
            except IndexError:
                print("no results for businessID: " + search_item)
                continue

            self.info = [['','','','','','','','','','','','','','','',''],\
                        ['','','','',''],\
                        [''],\
                        #30                         10                            20                            30                             40
                        ['','','','','','','','','','','','','','','','','',''\
                        ,'','','','','','','','','','','','','','','','','','','','','',''],\
                        [''],\
                        ['']\
                        ]

            if "BusinessSearch_BusinessInformation_lblEntityDetails" in driver.page_source:
                self.info[0] = self.grab_entity_info(driver.page_source.split("Entity Information")[2])
            if "BusinessSearch_BusinessInformation_lblStatutoryAgentInformation" in driver.page_source:
                self.info[1] = self.grab_agent_information(driver.page_source.split("Registered Agent Information")[1])
            if "BusinessSearch_BusinessInformation_lblPrincipalOfficeAddress" in driver.page_source:
                self.info[2] = self.grab_principal_office(driver.page_source.split("Principal Office Address")[1])
            if "BusinessSearch_BusinessInformation_lblPrincipalInformation" in driver.page_source:
                self.info[3] = self.grab_principal_info(driver.page_source.split("Principal Information")[1])
            if "BusinessSearch_BusinessInformation_lblShareInformation" in driver.page_source:
                self.info[4] = self.grab_total_shares(driver.page_source.split("Total Shares:</div>")[1])
            computation_time = time.time() - computation_time_1



            write_time_1 = time.time()
            file = open(self.write_file, 'a')
            for item in self.info[0]:
                file.write(Utils.build_quotes(item) + ",")
            for item in self.info[1]:
                file.write(Utils.build_quotes(item) + ",")
            for item in self.info[2]:
                file.write(Utils.build_quotes(item) + ",")

            for i in range(0, 40):
                if i < len(self.info[3]):
                    file.write(self.info[3][i] + ",")
                else:
                    file.write(Utils.build_quotes(self.infoBase[3][i]) + ",")
            for item in self.info[4]:
                file.write(Utils.build_quotes(item) + ",")
            write_time = time.time()-write_time_1

            web_lookup_time_2 = time.time()
            driver.find_elements_by_name("btnSearch")[0].send_keys(Keys.RETURN)
            web_lookup_time = web_lookup_time + (time.time()-web_lookup_time_2)

            computation_time_2 = time.time()
            try:
                self.info[5] = driver.page_source.split("bgwhite")[1][6:16]
            except IndexError:
                self.info[5] = "No Record"
            computation_time = computation_time + (time.time()-computation_time_2)

            write_time_2 = time.time()
            file.write(self.info[5]+"\n")
            file.close()
            write_time = write_time + (time.time() - write_time_2)


            name = self.info[0][0][:50]
            while len(name) < 50:
                name = name + " "
            total_time = time.time() - time1
            self.datapoints.append([int(search_item%self.search_iter),web_lookup_time,computation_time, write_time, total_time*3])
            print("grab " + str(search_item) + "\tbuilt-" + name , end='')
            print("web_time:" + str(web_lookup_time) + \
            "\tcalc_time:" + str(write_time)+\
            "\twrite_time:" + str(write_time)+\
            "\ttotal_time:" + str(total_time)
            )
    def retry_connection(driver, URL):
        print("connection error: waiting 10 seconds to reconnect")
        time.sleep(10)
        try:
            return driver.get(URL)
        except WebDriverException:
            self.retry_connection(driver, URL)
        return None

    def grab_entity_info(self, string):
        entity_name = string.split("Entity Name:</div>")[1].split(">")[1].split("<")[0]
        entity_ID = string.split("Entity ID:</label></div>")[1].split(">")[1].split("<")[0].strip()
        if entity_ID[0] == '0':
            entity_ID = "\'" + entity_ID
        entity_type = string.split("Entity Type:</div>")[1].split(">")[1].split("<")[0]
        if "Inactive" in string.split("Entity Status:</div>")[1].split("Formation Date:</div>")[0]:
            entity_status = "Inactive"
        elif "Active" in string.split("Entity Status:</div>")[1].split("Formation Date:</div>")[0]:
            entity_status = "Active"
        #entity_status = string.split("Entity Status:</div>")[1].split(">")[2].split("<")[0]
        formation_date = string.split("Formation Date:</div>")[1].split(">")[1].split("<")[0]
        reason_for_status = string.split("Reason for Status:</div>")[1].split(">")[1].split("<")[0]
        va_qual_date = string.split("VA Qualification Date:</div>")[1].split(">")[1].split("<")[0]
        status_date = string.split("Status Date:</a>")[1].split(">")[2].split("<")[0]
        industry_code = string.split("Industry Code:</div>")[1].split(">")[1].split("<")[0]
        duration_period = string.split("Period of Duration:</div>")[1].split(">")[2].split("<")[0]
        jurisdiction = string.split("Jurisdiction:</div>")[1].split(">")[1].split("<")[0]
        annual_report_due_date = string.split("Annual Report Due Date:</a>")[1].split(">")[2].split("<")[0]
        reg_fee_due_date = string.split("Registration Fee Due Date:</a>")[1].split(">")[2].split("<")[0]
        charter_fee = string.split("Charter Fee:</div>")[1].split(">")[1].split("<")[0]
        email = string.split("Email Address:</div>")[1].split(">")[1].split("<")[0]
        contact = string.split("Contact Number:</div>")[1].split(">")[1].split("<")[0]
        full_list = [entity_name, entity_ID, entity_type, entity_status, formation_date, reason_for_status, va_qual_date, status_date, industry_code, duration_period, jurisdiction, annual_report_due_date, reg_fee_due_date, charter_fee, email, contact]
        full_list = [x.strip() for x in full_list]
        return full_list

    def grab_agent_information(self, string):
        ra_type = string.split("RA Type:</div>")[1].split(">")[1].split("<")[0]
        locality = string.split("Locality:</div>")[1].split(">")[1].split("<")[0]
        ra_qual = string.split(r"RA Qualification</label>:</div>")[1].split(">")[1].split("<")[0]
        name = string.split("Name:</div>")[1].split(">")[1].split("<")[0]
        ra_address = string.split("Registered Office Address:</div>")[1].split(">")[1].split("<")[0]

        full_list = [ra_type,locality,ra_qual,name,ra_address]
        full_list = [x.strip() for x in full_list]
        return full_list

    def grab_principal_office(self, string):
        office_addr = string.split("Address:</div>")[1].split(">")[1].split("<")[0]
        full_list = [office_addr.strip()]
        return full_list

    def grab_principal_info(self, string):
        names = list()
        cut = re.split("bgwhite|bgrowalt", string)
        cut[len(cut)-1] = cut[len(cut)-1].split("</script")[0]
        finalcut = cut[1:]
        for item in finalcut:
            for piece in Utils.parseLine(item):
                names.append(piece)
        return names


    def grab_total_shares(self, string):
        shares = string.split(">")[1].split("<")[0].strip()
        return [shares]

    @staticmethod
    def build_graph(dataset_full,call):
        if not len(dataset_full) == 0:
            labels = ["web_time","calc_time","write_time", "total_time"]
            plots = [[dataset_full[i][l] for i in range(0, len(dataset_full))] for l in range(0,len(dataset_full[0]))]
            for i in range(1, len(plots)):
                plt.plot(plots[0], plots[i], 'o', label=labels[i-1])
            match = numpy.polyfit(plots[0][1:], plots[4][1:],1)
            p = numpy.poly1d(match)
            plt.plot(plots[0][1:], p(plots[0][1:]),"r--")
            plt.savefig(r"E:\DataSets\plt_" + str(call) + ".png")
            plt.close()
            #time.sleep(3)
            #plt.close(fig="all")
            return



m = VAScraper()
