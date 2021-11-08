import random
import math

class node:
    def __init__(self,value,next_layer_size):
        self.value = 0
        self.bias = random.random()
        self.weight_array = [random.random() for x in range(next_layer_size)]
        self.activation_function = 0

    def activate(self):
        self.activation_function = (double(1) / (1 + pow(2.71828182,-self.value+self.bias)))

    def __repr__(self):
        s = str(self.value) + " "
        s += str(self.weight_array)

        return s

    def push_to_layer(self,node_index):
        return((self.value+self.weight_array[node_index]))


class model:
    def __init__(self,input_size,output_size,layers):
        self.output_layer = [0 for x in range(output_size)]
        self.layers = []
        for layer in layers[:-1]:
            this_layer = []
            layer_index = layers.index(layer)
            next_layer_size = layers[layer_index+1]
            for x in range(layer):
                this_layer.append(node(0,next_layer_size))
            self.layers.append(this_layer)

        self.layers.append([node(0,output_size) for x in range(layers[-1])])
        self.input_layer = [node(0,layers[0]) for x in range(input_size)]

    def __repr__(self):
        string = ''
        string += str(self.input_layer)+"\n"
        for x in self.layers:
            string += str(x)
            string += "\n"
        string += str(self.output_layer)
        return string

    def push(self):

        for l in self.layers:
            index = self.layers.index(l)
            if self.layers.index(l) == 0:
                nodes_sum = []
                for node in l:
                    node_index = l.index(node)
                    sum = 0
                    for prev_node in self.input_layer:
                        sum += prev_node.value*prev_node.weight_array[node_index]+node.bias
                    node.value = sum

                #sums = [sum([node.push_to_layer(l.index(node2)) for node in self.input_layer]) for node2 in l]
            else:
                nodes_sum = []
                for node in l:
                    node_index = l.index(node)
                    sum = 0
                    for prev_node in self.layers[index-1]:
                        sum += prev_node.value*prev_node.weight_array[node_index]+node.bias
                    node.value = sum
                #sums = [sum([node.push_to_layer(l.index(node2)) for node in self.layers[index-1]]) for node2 in l]
        for x in self.output_layer:
            nodes_sum = []
            node_index = self.output_layer.index(x)
            sum = 0
            for prev_node in self.layers[-1]:
                sum += prev_node.value*prev_node.weight_array[node_index]
            self.output_layer[node_index] = sum
            #print(sums)
