import random
import math
import tensorflow
from tensorflow import keras
from tensorflow.keras.layers import *
import numpy

import matplotlib.pyplot as p


class model:
    def __init__(self,set_x,set_y):
        self.x = set_x
        self.y = set_y
        self.data_size = len(set_x)
        self.epochs = 5
        self.dpe = self.data_size*.9/self.epochs

        #self.normalize()
        self.build_datasets()

        self.x = numpy.asarray(self.x)
        self.y = numpy.asarray(self.y)

        self.train_x = self.x[:int(self.data_size*.90)]
        self.train_y = self.y[:int(self.data_size*.90)]


        self.test_x = self.x[int(self.data_size*.90):]
        self.test_y = self.y[int(self.data_size*.90):]
        guesses = {}
        self.model = keras.models.Sequential(\
                    [   Input(1,name='input'),\
                        Dense(16,activation='relu',name='hidden_layer1'),\
                        Dense(16,activation='relu',name='hidden_layer2'),\
                        Dense(1,activation='linear',name='output')\
                    ]
        )
        print(self.model.output_shape)

        model = keras.optimizers.Adam(learning_rate=.0001,epsilon=.00001)
        loss_function = 'mse'

        print("\n\nRUN 2")
        self.run_model(model,loss_function,self.epochs,self.dpe)
        self.check(random.randint(0,len(self.test_x)-1))

        print("while exec")
    def run_model(self,model,loss_function,e,s):
        try:
            self.model.compile(optimizer=model,loss=loss_function)
            self.model.fit(self.train_x,self.train_y,epochs=e,steps_per_epoch=s)
        except ValueError:
            print("encountered ValueError")
        self.model.summary()

    def check(self,i):
        print(i)
        print("ACTUAL: ")
        print(str(self.test_x[i]) + "->"+str(self.test_y[i]))
        y = self.model.predict([self.test_x[i]])
        print("MODEL: ")
        print(str(self.test_x[i]) + "->"+str(y))

        p.subplot(2,1,1)
        p.scatter(self.test_x,self.test_y,marker='o',label='actual')
        p.ylabel("actual")
        p.subplot(2,1,2)
        p.scatter(self.test_x,self.model.predict(self.test_x),marker='o')
        p.ylabel("predict")
        p.show()



    def normalize(self):
        self.max = 0
        for y in self.y:
            if y > self.max:
                self.max =  float(y)
        new_y = []
        for i in range(0,len(self.y)):
            new_y.append(self.y[i]/self.max)
        self.y = new_y

    def build_datasets(self):
        for r in range(0,int(self.data_size*.6)):
            i_2 = random.randint(0,self.data_size-1)
            i_1 = random.randint(0,self.data_size-1)
            temp_x = self.x[i_1]
            temp_y = self.y[i_1]
            self.x[i_1] = self.x[i_2]
            self.x[i_2] = temp_x
            self.y[i_1] = self.y[i_2]
            self.y[i_2] = temp_y

def build_file(filename):
    file = open(filename,'w')
    data_size = int(input("set size: "))
    #function = lambda x : math.sin(.2*x)+12*math.cos(2*x)+\
   #                       25*math.sin(.06*x)-12*math.cos(.4*x)
    function = lambda x : math.sin(x*.1)
    set_x = list(range(0,data_size))
    set_y = []

    for x in set_x:
        file.write(str(x) + " " + str(function(x)) + '\n')


if __name__  == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "b":
            build_file('text')
    file = open('text','r')
    x = []
    y = []
    for line in file.readlines():
        x.append(float(line.split(" ")[0]))
        y.append(float(line.split(" ")[1]))

    m = model(x,y)
