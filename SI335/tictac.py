import random
import numpy

class node:
    def __init__(self,input_size):
        self.vector = [random.uniform(0,1) for x in range(input_size)]
        self.value = 0
    def __repr__(self):
        master = '('
        for x in range(len(self.vector)):
            master += "%.4f "% self.vector[x]
        return master + str(self.value) + ")"

class neural_net:
    def __init__(self, layers, inputs):
        self.inputs = inputs
        self.layer = []
        for i in range(0, len(layers)):
            if i == 0:
                self.layer.append([node(inputs) for i in range(inputs)])
            else:
                self.layer.append([node(layers[i-1]) for x in range(layers[i])])
        self.layer.insert(0,[0 for x in range(inputs)])
    def feed(self,inputs):
        if not len(inputs) == self.inputs:
            print("bad inputs size: " + str(inputs) + ", need " + str(self.inputs))
        self.layer[0] = inputs
        for index in range(1,len(self.layer)):
            print(self.layer[index])
            for n in self.layer[index]:
                if (index-1) == 0:
                    vec_a = [x for x in self.layer[index-1]]
                else:
                    vec_a = [x.value for x in self.layer[index-1]]
                vec_b = [weight for weight in n.vector]
                val = numpy.dot(vec_a,vec_b)
                n.value = val

n = neural_net([1,2], 7)
print(n.layer)
n.feed([1,4,6,2,1,6,3])
print(n.layer)
