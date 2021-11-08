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

import re


class MNScraper:
    def __init__(self):
        self.URL = "https://mblsportal.sos.state.mn.us"
        self.URL_FIRST = "https://mblsportal.sos.state.mn.us/Business/BusinessSearch?BusinessName="
        self.URL_SECOND = "&IncludePriorNames=False&Status=Active&Type=BeginsWith"
        self.BusinessGrabs = list()
        self.items_grabbed = 0
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.write_file = r"C:\users\M226252\Desktop\FUllMNList.csv"
        self.build_search()
        self.scrape_into_csv()

    def build_search(self):
        self.search_list = list()
        for letter1 in "abcdefghijklmnopqrstuvwxyz":
            for letter2 in "abcdefghijklmnopqrstuvwxyz":
                for letter3 in "abcdefghijklmnopqrstuvwxyz":
                    self.search_list.append(str(letter1 + letter2 + letter3))
        print("built list")

    def scrape_into_csv(self):
        #, "--headless"
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=Utils.build_options(["--log-level=3", "headless", "user-agent="+self.user_agent]))
        #(file := open(self.write_file, "w")).write("BusinessName,Status,BusinessType,NameType,URL\n")
        #file.close()
        file = open(self.write_file, 'a')
        for i in range(self.search_list.index("hzb"), len(self.search_list)):
            search_item = self.search_list[i]
            num_writes = 0
            web_lookup_time_1 = time.time()
            driver.get(self.URL_FIRST + search_item + self.URL_SECOND)
            web_lookup_time_2 = computation_time_1 = time.time()
            names = driver.page_source.split("<strong>")[1:-2]
            try:
                types_pre_list = driver.page_source.split("table table-hover selectable")[1].split("<div class=\"row\">")[1:]
            except IndexError:
                print("no results for " + search_item)
                continue
            types = types_pre_list[2::3]
            status, business_type, name_type, business_name, URL = (None, None, None, None, None)
            urls = driver.page_source.split("table table-hover selectable")[1].split("searchResultsInfo")[0].split("a href=\"")[1:]
            if len(names) == len(urls):
                first_pass = [(names[i], urls[i]) for i in range(0, len(names))]
            else:
                print("mismatch Names and URLS on " + search_item + "\tnames:" + str(len(names)) + "\tURLS:" + str(len(urls)))
                continue

            for x, y in [(types[i], first_pass[i]) for i in range(0, len(types))]:
                dump = x.split("<span>")
                status = dump[1].split("</span")[0]
                business_type = dump[2].split("</span")[0]
                name_type = dump[3].split("</span")[0]
                name, URL = y
                business_name = name.split("</strong")[0].strip()
                URL = URL.split("\">Details")[0]
                if not (business_name, status, business_type, name_type, self.URL+URL) in self.BusinessGrabs:
                    self.BusinessGrabs.append((business_name, status, business_type, name_type, self.URL+URL))
                    self.items_grabbed = self.items_grabbed + 1
                    file = open(self.write_file, 'a')
                    try:
                        file.write(str(Utils.build_commas(business_name)) + "," + str(status) + "," + str(business_type)+ ","+ str(name_type)+ "," + str(self.URL+URL) +'\n')
                        file.close()
                        num_writes = num_writes + 1
                    except UnicodeEncodeError:
                        print("cant write entry:"+ str(num_writes+1))
                else:
                    print("found a duplicate"  + " " +str((business_name, self.URL+URL)))
            computation_time_2 = time.time()
            print("added: " + search_item + "\twrote: "+ str(num_writes) + "\ttotal: " + str(self.items_grabbed) + "\twebtime: " + str(web_lookup_time_2-web_lookup_time_1) + "\tcomputation_time: " + str(computation_time_2-computation_time_1))



m = MNScraper()




'''
        #, "--headless"
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=Utils.build_options(["--log-level=3", "headless", "user-agent="+self.user_agent]))
        for search_item in self.search_list:
            driver.get(self.URL_FIRST + search_item + self.URL_SECOND)
            names = driver.page_source.split("<strong>")[1:-2]
            types_pre_list = driver.page_source.split("table table-hover selectable")[1].split("<div class=\"row\">")[1:]
            types = types_pre_list[2::3]
            status, business_type, name_type, business_name, URL = (None, None, None, None, None)
            for x in types:
                dump = x.split("<span>")
                status = dump[1].split("</span")[0]
                business_type = dump[2].split("</span")[0]
                name_type = dump[3].split("</span")[0]
                print(str(status), str(business_type), str(name_type))

            urls = driver.page_source.split("table table-hover selectable")[1].split("searchResultsInfo")[0].split("a href=\"")[1:]
            first_pass = [(names[i], urls[i]) for i in range(0, len(names))]
            for name, URL in first_pass:
                business_name = name.split("</strong")[0].strip()
                URL = URL.split("\">Details")[0]
                print(str((business_name, status, business_type, name_type, self.URL+URL)))
                if not (business_name, status, business_type, name_type, self.URL+URL) in self.BusinessGrabs:
                    self.BusinessGrabs.append((business_name, status, business_type, name_type, self.URL+URL))
                    self.items_grabbed = self.items_grabbed + 1
                else:
                    print("found a duplicate"  + " " +str((business_name, self.URL+URL)))
            print("added " + str(len(self.BusinessGrabs)) + " businesses\ttotal " + str(self.items_grabbed))



'''
