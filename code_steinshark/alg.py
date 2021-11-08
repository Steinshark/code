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
from Utilities import Utilities as utils
from sklearn import metrics

from sklearn.neural_network import MLPClassifier



stock = list()

class Stock:
    def __init__(self, name):
        self.name = name
        self.day = list()
        self.earning = list()

### ADMIN
def login():
    username = "everetts"
    password = "NAVYlaptop52!!"
    r.authentication.login(username=username, password=password, mfa_code="MWSM5YI34RM2SLC4")
    print("successful login")

def logout():
    r.authentication.logout()
### ADMIN
def build_dataset():
    print("starting data")
    file1 = open("tickets", "r")

    for line in file1.readlines():
        name = line.rstrip()
        #build new file
        newFile = open("C:\\Users\\evere\\Desktop\\Code\\datasets\\" + name + ".csv", 'w')
        Hdata = r.get_stock_historicals(name, interval="day", span="5year")
        current = Stock(line)
        newFile.write("Date,Days,Open,Close,High,Low,Volume\n")

        for day in Hdata:
            try:
                #add to its own file
                l = day['begins_at'].split('-')
                date = (int(l[0]) - 2015)*365 + (int(l[1])*31) + (int(l[2][0:2]))
                newFile.write(str(day['begins_at']) + ',' + str(date) + ',' + str(day['open_price']) + ',' + str(day['close_price']) + ',' + str(day['high_price']) + ',' + str(day['low_price']) + ',' + str(day['volume']) + '\n')
            except TypeError:
                current = None
        stock.append(current)
        newFile.close()
    file1.close()
    print("added " + str(len(stock)) + " new entries")


def build_neural():
    write("preparing dataset with")
    options = True
    symbol = 'DHT'

    from sklearn import preprocessing

    x_train, x_test, y_train, y_test, dataframe, prediction = buildDataset(options, symbol)
    x_vector = (dataframe.iloc[:len(dataframe.values)-1, 2:len(dataframe.columns)-1]).values.tolist()
    y_vector = (dataframe.iloc[:len(dataframe.values)-1, len(dataframe.columns)-1:]).values.tolist()
    scaler = preprocessing.StandardScaler().fit(x_vector)
    x_vector = scaler.transform(x_vector)
    for int in range(0,len(y_vector)):
        y_vector[int] = y_vector[int][0]
    print(y_vector)
    lab_enc = preprocessing.LabelEncoder()
    y_vector = lab_enc.fit_transform(y_vector)
    #print("len x:" + str(len(x_vector)) + '\nlen y:' + str(len(y_vector)))

    network = MLPClassifier(solver='lbfgs', alpha=1e-4,hidden_layer_sizes=(128,64,32), random_state=1, max_iter=100000)
    print("starting fit")
    time1 = time.time()
    network.fit(x_vector,y_vector)
    print("fit took: " + str(time.time()-time1))
    print(network.predict((dataframe.iloc[len(dataframe.values)-1:, 2:len(dataframe.columns)-1]).values.tolist()))




def train(options, symbol):
    write("preparing dataset with")
    if not options:
        write("out")
    write(" options\n")

    x_train, x_test, y_train, y_test, dataframe, prediction = buildDataset(options, symbol)

    ## build and train our model
    write("building model\n")
    reg = RandomForestRegressor(n_estimators=1000, random_state=0)
    write("training\n")
    reg.fit(x_train, y_train)
    y_predictions = reg.predict(x_test)

    if True:
        for index in range(0, width := int(input('\nlook back how many days: '))):
            if index == 0:
                x_inputs = dataframe.iloc[:, 2:len(dataframe.columns)-1].tail(int(width)).values
                y_inputs = dataframe.iloc[:, len(dataframe.columns)-1].tail(int(width)).values
                y_inputs = list(map(lambda x : float("{:.2f}".format(x)), reg.predict(x_inputs)))
                #write('day\t\t\tPurchased\tActual' + str(prediction) + 'day\tActualProfit\tPredicted' + str(prediction) + 'Day\tPredictedProfit\n')
            #write(str(dataframe['Date'].tail(int(width)).values.tolist()[index])     + '\t')
            #write(str((dataframe['Close'].tail(int(width)).values.tolist()[index])) + '\t\t')
            #write("{:.2f}".format(dataframe.iloc[:, len(dataframe.columns)-1].tail(int(width)).values.tolist()[index]) + '\t\t')
            #write(str(float("{:.2f}".format(dataframe.iloc[:, len(dataframe.columns)-1].tail(int(width)).values.tolist()[index]-dataframe['Close'].tail(int(width)).values.tolist()[index]))) + '\t\t')
            #write(str(list(map(lambda x : float("{:.2f}".format(x)),y_inputs))[index]) + '\t\t')
            #write(str("{:.2f}".format(list(map(lambda x : float("{:.2f}".format(x)), y_inputs))[index]-float("{:.2f}".format(dataframe['Close'].tail(int(width)).values.tolist()[index])))) + '\n')


    ## how did we do?
    #write("MSE: "+  str(metrics.mean_squared_error(y_test, y_predictions)) + '\n')
    #write("MAE: " + str(metrics.mean_absolute_error(y_test, y_predictions)) + '\n')
    #write("RMSE: " + str(np.sqrt(metrics.mean_squared_error(y_test, y_predictions))) + '\n')


    write('\n\n\n')

    ### RESULTS ###
    lossCount,missCount,hitCount, profitCount = (0,0,0,0)
    for i in range(0, len(y_test)):
        #write("for buying at: " + str(x_test[i][2]) + "\tactual: " + str(y_test[i]) + "\tvs " + str(y_predictions[i]) + '\n')
        if (x_test[i][2] < y_predictions[i]) and (x_test[i][2] > y_test[i]):
            lossCount+=1
        if (x_test[i][2] > y_predictions[i]) and (x_test[i][2] < y_test[i]):
            missCount += 1
        if (x_test[i][2] < y_predictions[i]) and (x_test[i][2] <y_test[i]):
            hitCount += 1
        if (x_test[i][2] < y_test[i]):
            profitCount += 1

    write("losses: " + str(lossCount/len(y_test)) + '\nmisses: ' + str(missCount/len(y_test))+ '\nalg hits: ' + str(hitCount/len(y_test)) + "\ntotal hits:" +  str(profitCount/len(y_test)) + '\n')
    print((y_inputs.tail(1) - dataframe['Close'].tail(int(width)).values.tolist().tail(10).head(1)) / dataframe['Close'].tail(int(width)).values.tolist().head(10).tail(1))
    return (y_inputs.tail(1) - dataframe['Close'].tail(int(width)).values.tolist().tail(10).head(1)) / dataframe['Close'].tail(int(width)).values.tolist().head(10).tail(1)
    ### RESULTS ###






def buildDataset(options, symbol):
    try:
        dataframe = pd.read_csv("C:\\Users\\evere\\Desktop\\Code\\datasets\\" + symbol + ".csv")
    except FileNotFoundError:
        write("file not found...\n")
        return

    ### if no options are specified, then teh algorithm will default to adding 5, 20, and 100 day moving
    ### average data fields
    dayrange = [2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,100]
    daypeek = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,100]
    if not options:
        for day_range in dayrange:
            utils.add_EMA_field(dataframe, day_range)
        for pastdays in daypeek:
            utils.add_previous_close(dataframe, pastdays)

    ## with options, the user can specify adding which fields to add
    else:
        if (type := input('adding EMA? ')) in ['yes', 'Yes', 'y', 'Y', 'Standard','standard']:
            if type in ['Standard', 'standard']:
                pass
            else:
                 dayrange = input('add these ranges: ').split(' ')
            for day in dayrange:
                utils.add_EMA_field(dataframe, int(day))\

        if (type := input('adding Previous Close? ')) in ['yes', 'Yes', 'y', 'Y', 'standard', 'Standard']:
            if type in ['Standard', 'standard']:
                pass
            else:
                 daypeek = input('add these ranges: ').split(' ')

            for pastdays in daypeek:
                utils.add_previous_close(dataframe, pastdays)

    prediction = 10
    column_header = str(prediction := input("predict days ahead: ")) + ' Day Price'
    ## set default look-ahead at 20 days
    if not options:
        dataframe.insert(len(dataframe.columns),'10 Day Price', dataframe['Close'].shift(periods=-10).fillna(0))

    ## with options on, allows look-ahead to be specified
    ## 3-days ~15% predicts gain on actual loss
    ## 20-days ~3% predicts gain on actual loss
    else:
        column_header = str(prediction := input("predict days ahead: ")) + ' Day Price'
        dataframe.insert(len(dataframe.columns), column_header, dataframe['Close'].shift(periods=-int(prediction)).fillna(0))

    ## Build a plot for visuals by default
    #if not options:
        #dataframeNEW = dataframe[['Days', 'Close', 'EMA100Days']]
        #dataframeNEW.plot(x='Days')

    ## sanity check + debug
    #write(str(dataframe.head(30)) + '\n')
    plt.show(block=False)

    ## debug
    write("set built\n")
    buffer_lower = 100
    buffer_upper = len(dataframe[column_header]) - int(prediction)

    ## separate our data columns into dependent and independent data fields
    ## in this case, we want to predict column 9, our 20-day-price in the future
    x_data = dataframe.iloc[:, 2:len(dataframe.columns)-1][buffer_lower:buffer_upper].values
    #print(dataframe[buffer_lower:buffer_upper])
    y_data = dataframe.iloc[:, len(dataframe.columns)-1][buffer_lower:buffer_upper].values

    ## build the test and train data for the model
    write("building datasets\n")
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=.2, random_state=1)

    return (x_train, x_test, y_train, y_test, dataframe, prediction)

def algorithm():
    ## Load a list of all files
    filelist = list()
    buy_stock = list()
    for file in os.listdir("C:\\Users\\evere\\Desktop\\Code\\datasets"):
        filelist.append(open("C:\\Users\\evere\\Desktop\\Code\\datasets\\" + str(file), 'r'))

    #One by One open data of the file
    for opennedataframeile in filelist:
        #deal with all data in file
        buy_stock.append(opennedataframeile, decide(opennedataframeile))

    for stocks in stock:
        for dayStats in stocks.day:
            pass

def diagnose_data():
    x_train, x_test, y_train, y_test, frame, prediction = buildDataset(True, symbol := input("symbol"))
    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", 10000)
    print(frame.iloc[len(frame.values)-1:, :])



def write(string):
    avg = .3 / float(len(string))
    for letter in string:
        print(letter, end="", flush=True)
        if not avg < .01:
            time.sleep(avg)

def runAll():
    for symbol in open("C:\\Users\\evere\\Desktop\\Code\\tickets", 'r').readlines():
        if (return1 := train(False, symbol.rstrip('\n'))) >= .03:
            print(return1)


def run_alg():
    while (command := input(">>: ")) not in ["quit", "Quit", "exit", "Exit"]:
        if command == "build":
            build_dataset()
        elif command == "train":
            train((verbose := input("options? ")) in ['y', 'Y', 'yes', 'Yes'], input("symbol:"))
        elif command == "logout":
            logout()
        elif command == 'login':
            login()
        elif command == 'diag':
            diagnose_data()
        elif command == 'neural':
            build_neural()
        elif command == 'all':
            runAll()
        else:
            print("no match for command " + command)


run_alg()
