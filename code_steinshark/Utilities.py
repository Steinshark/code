import robin_stocks as r
from getpass import getpass
import os
import time

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import sklearn
import random

## this class is used to keep the algorithm file clean
class Utilities:

    ## adds an EMA field based off of the closing price of the stock
    @staticmethod
    def add_EMA_field(dataframe, timeperiod):
        column_header = 'EMA' + str(timeperiod) + 'Days'
        print('\t-added ' + column_header)
        column_header_delta = 'Delta EMA' + str(timeperiod)
        dataframe.insert(len(dataframe.columns),column_header, dataframe['Close'].ewm(span=timeperiod).mean(), True)
        dataframe.insert(len(dataframe.columns), column_header_delta, dataframe['Close'] - dataframe[column_header])

    @staticmethod
    def add_previous_close(dataframe, days_past):
        column_header = 'previous' + str(days_past)
        print('\t-added ' + column_header)
        column_header_delta = 'Delta Previous ' + str(days_past)
        dataframe.insert(len(dataframe.columns),column_header, dataframe['Close'].shift(int(days_past)).fillna(0), True)
        dataframe.insert(len(dataframe.columns), column_header_delta, dataframe['Close'] - dataframe[column_header])
