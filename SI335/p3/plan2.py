import random
import string
import pprint
import itertools
import time
import copy

class Target:
    def __init__(self, data, i):
        self.position = data[0:2]
        self.time_to_live = data[2]
        self.available = True
        self.name = string.ascii_uppercase[i]

    def update(self):
        self.time_to_live -= 1
        if self.time_to_live == -1:
            self.available = False

    def __repr__(self):
        return self.name + " " + str(str(self.position) + " @ " + str(self.time_to_live))

class Asset:
    def __init__(self,pos):
        self.position = pos

    def __repr__(self):
        return str(self.position)

class Plan:
    def __init__(self):
        self.targets = list()
        self.assets = list()
        self.obstacles = list()
        self.read_data()
        self.graph = Graph(self.assets,self.targets,self.obstacles,self.dimensions)
        self.graph.build_path()

    def read_data(self):
        filename = str(input("Map: "))
        file = open(filename,'r')

        #READ DIMENSIONS
        self.dimensions = [int(x) for x in file.readline().split(" ")]

        #READ OBSTACLES
        file.readline()
        for i in range(int(file.readline())):
            self.obstacles.append([int(x) for x in file.readline().split(" ")])

        #READ ASSETS
        file.readline()
        for i in range(int(file.readline())):
            self.assets.append(Asset([int(x) for x in file.readline().split(" ")]))

        #READ TARGETS
        file.readline()
        for i in range(int(file.readline())):
            self.targets.append(Target([int(x) for x in file.readline().split(" ")], i))

    def build_plan(self):
        pass

    def execute(self):
        pass

class Graph:
    class Node:
        def __init__(self,pos,type,ttl):
            self.pos = pos
            self.type = type
            self.discovered = False
            self.ttl = ttl
        def __repr__(self):
            return str(self.type)

    class Edge:
        def __init__(self,n1,n2,path):
            self.node1 = n1
            self.node2 = n2
            self.len = path[0]
            self.path = path[1]

        def __repr__(self):
            return str(self.node1) + "<->" + str(self.node2)

    def __init__(self,assets,targets,blocked,dimensions):
        t1 = time.time()
        self.radius_dep = True
        self.radius = 5000
        self.assets = assets
        self.targets = targets
        self.blocked = blocked
        self.dimensions = dimensions
        self.adjacency_list = {}
        self.build_nodes()
        self.build_edges()
        print("took " + str(time.time()-t1) + " to init")
    def build_nodes(self):
        # TAKES THE 2D GRAPH AND CREATES A NODE FOR EACH GRID SPACE
        self.nodes = []
        self.assetNodes = []
        self.targetNodes = []
        t_counts = 0
        asset_counts = 1
        for y in range(self.dimensions[0]):
            self.nodes.append(list())
            for x in range(self.dimensions[1]):
                temp = None
                if [y,x] in self.blocked:
                    temp = Graph.Node([y,x],'*',0)
                elif [y,x] in [x.position for x in self.targets]:

                    temp = Graph.Node([y,x], string.ascii_uppercase[t_counts],self.get_targ([y,x]).time_to_live)
                    self.targetNodes.append(temp)
                    t_counts += 1
                elif [y,x] in [x.position for x in self.assets]:
                    temp = Graph.Node([y,x],str(asset_counts),0)
                    self.assetNodes.append(temp)
                    asset_counts += 1
                else:
                    temp = Graph.Node([y,x],' ',0)
                self.nodes[y].append(temp)

    def build_edges(self):
        # BUILDS EDGES TO AND FROM NODES THAT ACTUALLY MATTER
        done = []
        for x in self.assetNodes+self.targetNodes:
            self.adjacency_list[x] = []
        for n1 in self.assetNodes + self.targetNodes:
            done.append(n1)
            nodes_from_n1 = self.big_bfs(n1, [x for x in self.targetNodes+self.assetNodes if not x in done])
            for n2 in nodes_from_n1.keys():
                dist, route = nodes_from_n1[n2]
                if not dist is None and not route is None:
                    self.adjacency_list[n1].append(Graph.Edge(n1,n2,(dist,route)))
                    self.adjacency_list[n2].append(Graph.Edge(n2,n1,(dist,self.reverse_path(route))))
    def build_path(self):
        need = len(self.targetNodes)
        for node in self.adjacency_list:
            if node in self.targetNodes:
                if len(self.adjacency_list[node]) == 0:
                    need -= 1
        # CREATES THE PATH BASED ON CLOSEST NODE FROM EACH OF THE ASSETS
        file = open(str(input("Moves: ")),'w')
        a = 0
        asset_fives = {}
        asset_moves = {}
        asset_location = {}
        asset_traveled = {}
        target_reached_at = {}

        ## INITIALIZE DICTIONARIES
        for asset in self.assetNodes:
            asset_fives[asset] = []
            asset_moves[asset] = []
            asset_location[asset] = asset
            asset_traveled[asset] = 0

        ## BUILD TARGET LISTS
        targeted = []
        while not len(targeted) == need:
            for asset in self.assetNodes:
                ## CHECK IF THIS NODE IS LEAST
                flag = False
                for asset2 in self.assetNodes:
                    if not asset == asset2:
                        if (asset_traveled[asset] > asset_traveled[asset2]):
                            flag = True
                if flag:
                    continue

                ## SOLVE NORMALLY
                if len(targeted) == len(self.targetNodes):
                    break
                this_edge, target = self.get_min(asset_location[asset],targeted)
                if this_edge is None:
                    continue
                targeted.append(target)

            ## ADD THE PATH DIRECIONS TO DICT
                asset_traveled[asset] += len(this_edge.path)
                for direction in this_edge.path:
                    asset_moves[asset].append(direction)
                asset_location[asset] = target
                asset_traveled[asset] += len(this_edge.path)

    ## WRITE DIRECTIONS TO FILE
        for i in range(0,1000):
            target = True
            for asset in self.assetNodes:
                if i >= len(asset_moves[asset]):
                    asset_location[asset], dir = self.get_safe_edge(asset_location[asset])
                    #print("is safe: " + str(dir))
                    file.write(dir)
                else:
                    file.write(asset_moves[asset][i])
            file.write("\n")
        file.close()

    def get_min(self,node,already):
        min = 100000
        min_edge = None
        for edge in self.adjacency_list[node]:
            if edge.node2 in already or edge.node2 in self.assetNodes:
                continue
            elif edge.len < min:
                min = edge.len
                min_edge = edge
        if not min_edge is None:
            return min_edge, min_edge.node2
        else:
            return None, None

    def get_safe_edge(self,node):
        node_list = self.get_neighbors(node.pos[0],node.pos[1])
        num = random.randint(0,3)
        node2,dir = node_list[num]
        while node2 is None:
            num = random.randint(0,3)
            node2, dir = node_list[num]
        return node_list[num]

    def reverse_path(self,path):
        new_path = []
        for direction in reversed(path):
            if direction == "U":
                new_path.append("D")
            elif direction == "D":
                new_path.append("U")
            elif direction == "R":
                new_path.append("L")
            elif direction == "L":
                new_path.append("R")
        return new_path

    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def get_neighbors(self,y,x):
        n = None
        s = None
        e = None
        w = None
        if not y-1 == -1 and not self.nodes[y-1][x].type == '*':
            n = self.nodes[y-1][x]
        if not y+1 >= self.dimensions[0] and not self.nodes[y+1][x].type == '*':
            s = self.nodes[y+1][x]
        if not x+1 >= self.dimensions[1] and not self.nodes[y][x+1].type == '*':
            e = self.nodes[y][x+1]
        if not x-1 == -1 and not self.nodes[y][x-1].type == '*':
            w = self.nodes[y][x-1]
        return ((n,"U"),(s,"D"),(e,"R"),(w,"L"))

    def bfs(self,node_a,node_b):
        open = [node_a]
        discovered = {node_a:True}
        parents = {}
        while not len(open) == 0:
            node = open.pop(0)
            if node == node_b:
                path = []
                p = parents[node]
                while not p[0] == node_a:
                    path.insert(0,p[1])
                    p = parents[p[0]]
                path.insert(0,p[1])
                return (len(path), path)
            else:
                for neighbor,direction in self.get_neighbors(node.pos[0], node.pos[1]):
                    if not neighbor is None and not neighbor in discovered:
                        parents[neighbor] = (node,direction)
                        discovered[neighbor] = True
                        open.append(neighbor)

    def big_bfs(self,node_a,incomplete):
        open = [node_a]
        paths = {x : (None,None) for x in incomplete}
        discovered = {node_a:True}
        parents = {}
        while (None,None) in paths.values() and not len(open) == 0:
            node = open.pop(0)
            if node in incomplete:
                path = []
                p = parents[node]
                while not p[0] == node_a:
                    path.insert(0,p[1])
                    p = parents[p[0]]
                path.insert(0,p[1])
                paths[node] = (len(path), path)

            for neighbor,direction in self.get_neighbors(node.pos[0], node.pos[1]):
                if not neighbor is None and not neighbor in discovered:
                    parents[neighbor] = (node,direction)
                    discovered[neighbor] = True
                    open.append(neighbor)
        return paths

    def get_edge(self,n1,n2):
        for edge in self.adjacency_list[n1]:
            if edge.node2 == n2:
                return edge

    def get_targ(self,pos):
        for target in self.targets:
            if target.position[0] == pos[0] and target.position[1] == pos[1]:
                return target
    def naive(self):
        self.graph_verts = {x : [] for x in self.assetNodes}
        self.graph_starts = {x : self.get_min(x,[]) for x in self.assetNodes}
        self.best_score
        print(self.graph_verts)
        print(self.graph_starts)
        self.naive_recursive([],self.targetNodes,0)

    def naive_recursive(self,nodes,remaining,score):
        ## Base case
        if len(remaining) == 0:
            cur += self.get_edge(nodes[-1],nodes[0])
            if score < self.best_cost:
                self.best_score = score
                self.best_path = copy.copy(nodes)

        ## Not a better case (cut tree)
        elif cur >= self.best_score:
                return

        ## continue recursing
        else:
            for node in remaining:
                edge = self.get_edge(nodes[-1],node)
                iter_rem = copy.deepcopy(remaining)
                iter_nodes = copy.deepcopy(nodes)
                for nodes in iter_rem:
                    nodes.ttl -= edge.len
                if node.ttl - edge.len > 0:
                    score += node.ttl - edge.len
                iter_rem.remove(node)
                naive_recursive(iter_nodes,iter_rem,score)

    def min_loss(self):
        self.graph_verts = {x : [x] for x in self.assetNodes}
        self.min_loss = 99999
        self.min_loss_rec(copy.copy(self.graph_verts),copy.copy(self.targetNodes),0)
        print(self.min_loss)
    def min_loss_rec(self,verts,remaining,loss):

        if len(remaining) == 0:
            if loss < self.min_loss:
                self.graph_verts = verts
                self.min_loss = loss
                print("New min == " + str(loss))
            print("ended at " + str(verts))
            return
        elif loss > self.min_loss:
            print("past min")
            return
        else:
            for n2 in remaining:
                for asset in verts.keys():
                    iter_verts = {x : copy.copy(verts[x]) for x in verts.keys()}

                    n1 = iter_verts[asset][-1]
                    print(str(n1) + " to " + str(n2))
                    cost = self.get_edge(n1,n2).len
                    deaths = [node.ttl for node in remaining if node.ttl < cost]

                    iter_rem = [x for x in remaining if not x == n2 and not x in deaths]
                    iter_verts[asset].append(n2)

                    loss += len(iter_rem)*cost + sum(deaths) + cost
                    self.min_loss_rec(iter_verts,iter_rem,loss)



p = Plan()
