import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from string import ascii_uppercase
from string import ascii_lowercase
import tkinter
import string
import time
import re
import pandas
import matplotlib.pyplot as plt
import numpy
class Utils:
####################################################################################################
#                                           CONSTANTS                                              #
####################################################################################################
    FILENAME = "C:\\Users\\evere\\Downloads\\Virginia A-Bennett.csv"
    WEBSITE = r"https://cis.scc.virginia.gov"
    requestURL = "https://cis.scc.virginia.gov/EntitySearch/Index"
    BusinessIDURL = "https://cis.scc.virginia.gov/EntitySearch/BusinessPrincipalsList"
    replacements = {
        "Ln " : "Lane ",
        "Ln." : "Lane ",
        " Ln" : " Lane ",

        "Dr ": "Drive ",
        "Dr.": "Drive ",

        "St ":"Street ",
        "St.":"Street ",

        "Rd " : "Road ",
        "Rd." : "Road ",
        " Rd" : " Road ",

        "Ct " : "Court ",
        "Ct." : "Court ",
        " Ct " : " Court ",

        "Ctr " : "Center ",
        "Cntr" : "Center",

        "Cir " : "Circle ",
        "Cir." : "Circle ",

        "Pl " : "Place ",
        "Pl." : "Place ",

        "Blvd" : "Boulevard ",
        "Blvd." : "Boulevard ",
        " Blvd" : " Boulevard ",

        "Ave " : "Avenue ",
        "Ave. " : "Avenue ",
        "Ave." : "Avenue",

        "Ste " : "#",
        "Apartment" : "#",
        "Apt" : "#",

        "Unit " : "#",
        "Suite " : "#",

        "Sq " : "Square",
        "Sq." : "Square",

        "North" : "N",
        "South" : "S",
        "East" : "E",
        "West" : "W",

        "N." : "N",
        "S." : "S",
        "E." : "E",
        "W." : "W",

        " Ne " : " NE ",
        "Nw " : "NW ",
        " Se " : " SE ",
        "Sw " : "SW ",

        "Va " : "VA",

        "Iii" : "III",
        "Iv" : "IV",
        "Ii" : "II",


        "#" : " #"
         }

    suffix_list = [
        "Jr ",
        "Sr "
        ]

    President = ["President", "president", "pres", "Pres",]
    Treasurer = ["Treasurer", "treasurer", "Treas", "treas"]
    Secretary = ["Secretary", "secretary", "Sec", "sec", "SEC"]
    Vice_President = ["Vice"]





####################################################################################################
#                                           /CONSTANTS                                             #
####################################################################################################
    @staticmethod
    def scrub_address(address_raw):
        #split address into comma separated list
        splitAddress = address_raw.split(',')


        #for the extra comma case
            #replace all instances of abbreviations in address that are not at the end
        house_number = ""
        city = ""
        state = ""
        zip = ""
        foreign = "False"
        country = "USA"
        #handle the address formatting in this section.
        check = list()
        for x in splitAddress:
            for n in x.split(" "):
                check.append(n)
        if "Foreign" in check:
            foreign = "True"
            country = 'USA'
            if len(splitAddress) == 7:
                house_number = splitAddress[0]
                city = splitAddress[1].split(" ")[0]
                state = splitAddress[1].split(" ")[1]

                zip = " "

            elif len(splitAddress) == 9:
                house_number = splitAddress[0]
                city = splitAddress[1]
                state = splitAddress[2]
                zip = splitAddress[3]
                country = splitAddress[4]

            else:
                print("another case: " + str(splitAddress))
        else:
            if len(splitAddress) == 4:
                house_number = str(splitAddress[0])
                if len(splitAddress[1].strip()) == 2:
                    splitAddress.insert(1, "")
                if len(splitAddress[1].split(" ")) > 1:
                    house_number = house_number + splitAddress[1]
                else:
                    #print("really weird addr input on: " + str(splitAddress))
                    city = ""
                    state = splitAddress[2].strip()
                    zip = splitAddress[3].strip()[:5]
                    #print("house: " + str(house_number)  + ", city: " + str(city) + ", state: " + str(state) + ", zip: " + str(zip) )

                state = splitAddress[2].strip()
                zip = splitAddress[3].title().strip()[0:5]

            if len(splitAddress) == 5:
                house_number = str(splitAddress[0])
                city = splitAddress[1].title().strip()
                state = splitAddress[2].strip()
                zip = splitAddress[3].title().strip()[0:5]

            elif len(splitAddress) == 6:
                house_number = str(splitAddress[0]) + str(splitAddress[1])
                city = splitAddress[2].title().strip()
                state = splitAddress[3].strip()
                zip = splitAddress[4].title().strip()[0:5]

            elif len(splitAddress) == 7:
                house_number = str(splitAddress[0]) + str(splitAddress[1]) + str(splitAddress[2])
                city = splitAddress[3].title().strip()
                state = splitAddress[4].strip()
                zip = splitAddress[5].title().strip()[0:5]
            elif len(splitAddress) == 8:
                house_number = str(splitAddress[0]) + str(splitAddress[1]) + str(splitAddress[2]) + str(splitAddress[3])
                city = splitAddress[4].title().strip()
                state = splitAddress[5].strip()
                zip = splitAddress[6].title().strip()[0:5]



        house_number = string.capwords(house_number.strip(), " ")

        for letter in ascii_lowercase:
            house_number = house_number.replace("#"+letter, "#"+letter.upper())

        for initial, full in Utils.replacements.items():
            house_number = house_number.replace(initial, full).replace("  ", " ")

        #replace all instances of abbreviations that ARE at the end
        if house_number[-2:] == "Dr":
            house_number = house_number[:-2] + "Drive"
        if house_number[-2:] == "St":
            house_number = house_number[:-2] + "Street"
        if house_number[-2:] == "Pl":
            house_number = house_number[:-2] + "Place"
        if house_number[-3:] == "Cir":
            house_number = house_number[:-3] + "Circle"
        if house_number[-3:] == "Ave":
            house_number = house_number[:-3] + "Avenue"
        if house_number[-2:] == "Sq":
            house_number = house_number[:-3] + "Square"

        #print("sending " + str([house_number, city, state, zip]))
        return [foreign,house_number,city, state, zip, country]
        #return scrubbed string

    @staticmethod
    def scrub_name(name_raw):

        name_raw = name_raw.title().replace("  ", " ").strip().replace(".", "")
        if name_raw[0] in ascii_uppercase and name_raw[1] == ' ':
            name_raw = name_raw[0] + "." + name_raw[1:]
        for letter in ascii_uppercase:
            name_raw = name_raw.replace(" " + letter + " ", " " + letter + ". ")
        for suffix in Utils.suffix_list:
            name_raw = name_raw.replace(" " + suffix, ", " + suffix + ".")

        if name_raw[-2:] == "Jr":
            name_raw = name_raw[:-2] + "Jr."
        if name_raw[-2:] == "Sr":
            name_raw = name_raw[:-2] + "Sr."

        return name_raw

    @staticmethod
    def scrub_title(title_raw):
        for title in Utils.President:
            if title in title_raw and not "V" in title_raw:
                return "President"
        for title in Utils.Treasurer:
            if title in title_raw:
                return "Treasurer"
        for title in Utils.Secretary:
            if title in title_raw:
                return "Secretary"
        for title in Utils.Vice_President:
            if title in title_raw:
                return "Vice President"
        return "Director"

    @staticmethod
    def scrub_type(type_raw):
        type_raw = type_raw.strip()
        if type_raw == "Hoa":
            return "HOA"
        return type_raw

    @staticmethod
    def build_quotes(string):
        return '\"' + string + '\"'

    @staticmethod
    def get_file_name(string):
        liszt = string.split('/')
        return liszt[len(liszt)-1]


    @staticmethod
    def write(writer, string):
        writer.insert(tkinter.END, string)
        writer.yview(tkinter.END)

    @staticmethod
    def build_options(options):
        chrome_options = Options()
        for option in options:
            chrome_options.add_argument(option)
        return chrome_options


    @staticmethod
    def parseLine(string):
    ########################################################################################################
        ParsedData = list()

        if not len(re.split("<td|<Td", string)) <= 2:
            #HTML columns in a row are separated by a "<td>" tag.
            # splts each row into its separate data field
            words = re.split("<td|<Td", string)
            ParsedData.append(Utils.build_quotes(Utils.scrub_name(words[3].split("<")[0][1:].title())))
            #must be encoded in quotes because contains ','
            addressFull = words[4].split("<")[0][1:]
            final_address_list = Utils.scrub_address(Utils.build_quotes(addressFull))
            ##          Foreign     ##
            ParsedData.append(Utils.build_quotes(final_address_list[0]))
            ##          address     ##
            ParsedData.append(Utils.build_quotes(final_address_list[1]))
            ##          City        ##
            ParsedData.append(Utils.build_quotes(final_address_list[2]))
            ##          State       ##
            ParsedData.append(Utils.build_quotes(final_address_list[3]))
            ##          Zip         ##
            ParsedData.append(Utils.build_quotes(final_address_list[4]))
            ##          country     ##
            ParsedData.append(Utils.build_quotes(final_address_list[5]))
            ##          title       ##
            ParsedData.append(Utils.build_quotes(Utils.scrub_title(words[1][1:].split("<")[0].title())))
        return ParsedData
