import random
import copy

A = {"A":0.0,"B":4.3,"C":5.1,"D":4.6,"E":8.1,"F":3.8,"G":5.5,"H":7.3,"I":6.8,"J":5.7}
B = {"A":4.3,"B":0.0,"C":3.6,"D":6.1,"E":4.4,"F":3.5,"G":1.5,"H":5.4,"I":2.6,"J":5.5}
C = {"A":5.1,"B":3.6,"C":0.0,"D":3.5,"E":4.0,"F":1.4,"G":3.1,"H":2.2,"I":5.3,"J":2.1}
D = {"A":4.6,"B":6.1,"C":3.5,"D":0.0,"E":7.5,"F":2.7,"G":6.3,"H":4.8,"I":8.4,"J":2.2}
E = {"A":8.1,"B":4.4,"C":4.0,"D":7.5,"E":0.0,"F":5.2,"G":3.0,"H":3.5,"I":3.8,"J":5.6}
F = {"A":3.8,"B":3.5,"C":1.4,"D":2.7,"E":5.2,"F":0.0,"G":3.6,"H":3.6,"I":5.7,"J":2.3}
G = {"A":5.5,"B":1.5,"C":3.1,"D":6.3,"E":3.0,"F":3.6,"G":0.0,"H":4.4,"I":2.2,"J":5.2}
H = {"A":7.3,"B":5.4,"C":2.2,"D":4.8,"E":3.5,"F":3.6,"G":4.4,"H":0.0,"I":6.3,"J":2.6}
I = {"A":6.8,"B":2.6,"C":5.3,"D":8.4,"E":3.8,"F":5.7,"G":2.2,"H":6.3,"I":0.0,"J":7.4}
J = {"A":5.7,"B":5.5,"C":2.1,"D":2.2,"E":5.6,"F":2.3,"G":5.2,"H":2.6,"I":7.4,"J":0.0}

graph = {"A":A,"B":B,"C":C,"D":D,"E":E,"F":F,"G":G,"H":H,"I":I,"J":J}

iter = 0
def build(current_node, node_progression,best_progression, current_size,best_yet):
    if len(node_progression) == len(graph):
        #print("\t\tPUSHING BACK UP")
        if current_size + graph[current_node][node_progression[0]] <= best_yet:
            print("\t\tUPDATING: " + str(node_progression) + " " + str(current_size + graph[current_node][node_progression[0]]))
            return (node_progression, current_size + graph[current_node][node_progression[0]])
        else:
            #print("\t\t MAINTAIN: " + str(best_progression) + " " + str(best_yet))
            #print("\t\tCURRENT IS: " + str(node_progression) + " " + str(current_size))
            return (best_progression, best_yet)
    else:
        for n in [node for node in list(graph[current_node].keys()) if not node in node_progression and not node == current_node]:
            b = copy.deepcopy(best_progression)
            t = copy.deepcopy(node_progression)
            t.append(n)
            if not current_size + graph[current_node][n] > best_yet:
                best_progression, best_yet = build(n,t,b, current_size + graph[current_node][n],best_yet)
            else:
                "pruned it"
        return best_progression, best_yet

max = (None,1000)
for node in graph.keys():
    a, b = build(node,[node],[],0,1000)
    if b < max[1]:
        max = (a,b)
print(max)
