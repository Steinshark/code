import random
import numpy as np
import math
import copy
import tac
import string
import decimal


class Node:
    def __init__(self,next_layer_size):
        self.value = 0
        self.weight = [round(random.random(),5) for x in range(next_layer_size)]

    def __repr__(self):
        return str(format(self.value,".2f")) + str(self.weight)


class model:
    def __init__(self,input_size,layers,output_size):
        ## Constants
        self.input_size = input_size
        self.hidden_layers_count = len(layers)
        self.output_size = output_size
        self.moves = 0

        ## Layer build
        self.input_layer = [Node(layers[0]) for x in range(input_size)]
        self.hidden_layers =[]
        for size in range(len(layers[:-1])):
            self.hidden_layers.append([Node(layers[size+1]) for x in range(layers[size])])
        self.hidden_layers.append([Node(output_size) for x in range(layers[-1])])
        self.output_layer = [Node(1) for x in range(output_size)]

    def __repr__(self):
        master_s = ''
        for item in self.input_layer:
            master_s += (str(item) + ' ')
        master_s += '\n'
        for x in self.hidden_layers:
            master_s += (str(x) + "\n")

        master_s += str(self.output_layer)
        return master_s

    def get_rules(self):
        max_i = self.get_max_index()
        max = self.get_max_value()
        final_layer = self.hidden_layers[-1]

        rand_node_index = random.randrange(len(final_layer))

        old_weight = final_layer[rand_node_index].weight[max_i]

        final_layer[rand_node_index].weight[max_i] = .95*final_layer[rand_node_index].weight[max_i]
        return

        i = 0
        while self.get_max_value() >= max:
            if i > 100:
                return
            final_layer[rand_node_index].weight[max_i] = old_weight
            final_layer[rand_node_index].weight[max_i] = random.random()
            self.forward_propogate()
            i += 1

        return

    def improve_rules(self):
        max_i = self.get_max_index()
        max = self.get_max_value()
        final_layer = self.hidden_layers[-1]

        rand_node_index = random.randrange(len(final_layer))

        old_weight = final_layer[rand_node_index].weight[max_i]

        i = 0
        final_layer[rand_node_index].weight[max_i] = 1.2*final_layer[rand_node_index].weight[max_i]
        return
        while self.get_max_value() <= max:
            if i > 100:
                return
            final_layer[rand_node_index].weight[max_i] = old_weight
            final_layer[rand_node_index].weight[max_i] = random.random()
            self.forward_propogate()
            i += 1

        return

    def change_rand(self):
        size = 1 + self.hidden_layers_count

        selection = random.randrange(size)
        if selection == 1:
            size = random.randrange(self.input_size)
            self.input_layer[size].weight[random.randrange(len(self.input_layer[size].weight))] = random.random()
        else:
            layer = random.randrange(size-1)
            node = random.randrange(len(self.hidden_layers[layer]))
            self.hidden_layers[layer][node].weight[random.randrange(len(self.hidden_layers[layer][node].weight))] = random.random()

    def fill(self,inputs):
        if not len(inputs) == self.input_size:
            print("input size of " + str(len(inputs)) + " does not match model size of " + str(self.input_size))
        for i in range(len(inputs)):
            self.input_layer[i].value = inputs[i]

    def train(self,x_set,y_set):
        for x_item in x_set:
            if not len(x_item) == self.input_size:
                print("Bad input size of " + str(len(x_item)) + "for model of size " + str(self.input_size))
                return
        for y_item in y_set:
            if not len(y_item) == self.output_size:
                print("Bad output size of " + str(len(y_item)) + "for model of size " + str(self.output_size))
                return


        for x_item in x_set:
            self.fill(x_item)
            self.forward_propogate()

    def forward_propogate(self):
        summation = 0

        ## UPDATE FIRST HIDDEN LAYER OF MODEL
        for i in range(len(self.hidden_layers[0])):
            summation = sum([node.value*node.weight[i] for node in self.input_layer])
            self.hidden_layers[0][i].value = self.activate(summation)


        ## UPDATE ALL HIDDEN LAYERS OF MODEL
        for layer in self.hidden_layers[1:]:
            for i in range(len(layer)):
                summation = sum([node.value*node.weight[i] for node in self.hidden_layers[self.hidden_layers.index(layer)-1]])
                layer[i].value = self.activate(summation)


        ## UPDATE OUTPUT LAYER
        for i in range(len(self.output_layer)):
            summation = sum([node.value*node.weight[i] for node in self.hidden_layers[-1]])
            self.output_layer[i].value = self.activate(summation)

    def save_to_file(self,fname):
        file = open(fname,"w")
        for node in self.input_layer:
            for weight_part in node.weight:
                file.write(str(weight_part) + ",")
            file.write("|")
        file.write("\n")
        for layer in self.hidden_layers:
            for node in layer:
                for weight_part in node.weight:
                    file.write(str(weight_part) + ",")
                file.write("|")
            file.write("\n")

        file.write(str(self.output_size))
        file.close()

    def build_from_file(f_name):
        file = open(f_name,"r")
        full = file.readlines()
        in_layer = full[0][:-3].split("|")
        #print(in_layer)
        in_weights = []
        for node in in_layer:
            weight = node.split(",")[:-1]
            weight = [float(decimal.Decimal(x)) for x in weight]
            in_weights.append(weight)

        layers = []
        for layer in full[1:-1]:
            layer = layer[:-2]
            this_layer = layer.split("|")
            in_weights = []
            for node in this_layer:
                weight = node.split(",")[:-1]
                weight = [float(decimal.Decimal(x)) for x in weight]
                in_weights.append(weight)
            layers.append(in_weights)




        #print(in_weights)
        #print("IN_LAYER HAS " + str(len(in_weights)) + " NODES OF LEN " + str(len(in_weights[0])))
        #print("THERE ARE " + str(len(layers)) + " HIDDEN LAYERS " + str(len(layers[0])) + " " + str(len(layers[1])) + " " + str(len(layers[2])))


        out_layer = int(full[-1].rstrip())


        #print(layers[0])

        machine = model(len(in_weights),[len(x) for x in layers],out_layer)

        for i in range(len(machine.input_layer)):
            machine.input_layer[i].weight = in_weights[i]

        for i in range(machine.hidden_layers_count):
            for j in range(len(machine.hidden_layers[i])):
                 machine.hidden_layers[i][j].weight = layers[i][j]

    def activate(self,summation):
        return 1/(1+ math.pow(math.e,-summation))

    def get_max(self):
        max = Node(1)
        for node in self.output_layer:
            if node.value > max.value:
                max = node
        i = self.output_layer.index(max)

        returning_str = str(string.ascii_lowercase[(i//3)]) + str(i%3)
        return returning_str

    def get_max_index(self):
        max = Node(1)
        for node in self.output_layer:
            if node.value > max.value:
                max = node
        i = self.output_layer.index(max)
        return i

    def get_max_value(self):
        cur = 0
        for x in [node.value for node in self.output_layer]:
            if x > cur:
                cur = x
        return cur

def random_training(machine):
    m_copy = copy.deepcopy(machine)

def iterate_sequence(m_x,m_o,game,iters,x_wins,o_wins):
    for i in range(iters):
        if (i % 1000) == 0:
            print(str(i) + " iterations")

        if game.on_player == 'x':
            m_x.fill(game.translate_to_array())
            m_x.forward_propogate()
            move = m_x.get_max()

            if not game.check_mov(move):
                m_x.get_rules()
                iters += 1
                game = tac.Board()
                continue

            game.play_mov(move)
            game.moves += 1
            m_x.moves += 1

        elif game.on_player == 'o':
            m_o.fill(game.translate_to_array())
            m_o.forward_propogate()
            move = m_o.get_max()

            if not game.check_mov(move):
                m_o.get_rules()
                iters += 1
                game = tac.Board()
                continue

            game.play_mov(move)
            game.moves += 1
        else:
            print("strange exception on game player on")

        game.game_over, game.winner = game.check_win()

        if game.game_over:
            if game.winner == 'o':
                o_wins += 1
            else:
                x_wins += 1
            game = tac.Board()

def run_verbose(m_x,m_o,game,iters,x_wins,o_wins):
        for i in range(iters):
            if (i % 1000) == 0:
                print(str(i) + " iterations")

            if game.on_player == 'x':
                m_x.fill(game.translate_to_array())
                m_x.forward_propogate()
                move = m_x.get_max()

                if not game.check_mov(move):
                    m_x.get_rules()
                    iters += 1
                    game = tac.Board()
                    input()
                    print(game)
                    continue

                m_x.improve_rules()
                game.play_mov(move)
                print(game)
                input()
                game.moves += 1
                m_x.moves += 1

            elif game.on_player == 'o':
                m_o.fill(game.translate_to_array())
                m_o.forward_propogate()
                move = m_o.get_max()

                if not game.check_mov(move):
                    m_o.get_rules()
                    iters += 1
                    game = tac.Board()
                    input()
                    print(game)
                    continue

                m_o.improve_rules()
                game.play_mov(move)
                print(game)
                input()
                game.moves += 1
            else:
                print("strange exception on game player on")

            game.game_over, game.winner = game.check_win()

            if game.game_over:
                if game.winner == 'o':
                    o_wins += 1
                else:
                    x_wins += 1
                game = tac.Board()

def execute_command_sequence():
    m_x = model(9,[3,3,9],9)
    m_o = model(9,[3,3,9],9)
    x_wins = 0
    o_wins = 0

    game = tac.Board()

    models = 0

    command = input(": ")

    while not command == "quit":
        if command == "iterate":
            iterate_sequence(m_x,m_o,game,int(input("iterations: ")),x_wins,o_wins)
        elif command == "save":
            m_x.save_to_file(input("filename_x: "))
            m_o.save_to_file(input("filename_o: "))
        elif command == "load":
            m_x = model.build_from_file(input("fname_x: "))
            m_o = model.build_from_file(input("fname_o: "))
        elif command == "show":
            run_verbose(m_x,m_o,game,1,x_wins,o_wins)
        elif command == "model":
            if input("model: ") == "x":
                print(m_x)
            else:
                print(m_o)
        command = input(": ")




print("starting")

execute_command_sequence()
