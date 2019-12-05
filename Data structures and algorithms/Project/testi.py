# A Python program for Prim's Minimum Spanning Tree (MST) algorithm. 
# The program is for adjacency matrix representation of the graph 

import sys # Library for INT_MAX 
import os

class Graph(): 
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = [[0 for column in range(vertices)] 
                        for row in range(vertices)] 

    def minKey(self, key, mstSet): 

        # Initilaize min value 
        min = sys.maxsize 

        for v in range(self.V): 
            if key[v] < min and mstSet[v] == False: 
                min = key[v] 
                min_index = v 

        return min_index

    def printMST(self, parent): 
        f = open("temp.txt","w")
        for i in range(1, self.V):
            f.write("{} {} {}\n".format(parent[i] + 1, i + 1, self.graph[i][ parent[i] ]))
        f.close()

    # Function to construct and print MST for a graph 
    # represented using adjacency matrix representation 
    def primMST(self): 

        # Key values used to pick minimum weight edge in cut 
        key = [sys.maxsize] * self.V 
        parent = [None] * self.V # Array to store constructed MST 
        # Make key 0 so that this vertex is picked as first vertex 
        key[0] = 0
        mstSet = [False] * self.V 

        parent[0] = -1 # First node is always the root of 

        for cout in range(self.V): 

            # Pick the minimum distance vertex from 
            # the set of vertices not yet processed. 
            # u is always equal to src in first iteration 
            u = self.minKey(key, mstSet) 

            # Put the minimum distance vertex in 
            # the shortest path tree 
            mstSet[u] = True

            # Update dist value of the adjacent vertices 
            # of the picked vertex only if the current 
            # distance is greater than new distance and 
            # the vertex in not in the shotest path tree 
            for v in range(self.V): 
                # graph[u][v] is non zero only for adjacent vertices of m 
                # mstSet[v] is false for vertices not yet included in MST 
                # Update the key only if graph[u][v] is smaller than key[v] 
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]: 
                        key[v] = self.graph[u][v] 
                        parent[v] = u 

        self.printMST(parent) 

def nollaverkko(pituus):
    nolla = []
    rivi = []
    for i in range(0, pituus):
        for j in range(0, pituus):
            rivi.append(0)
        nolla.append(rivi)
        rivi = []
    return nolla

def muodosta_verkko(lista):
    rivi = lista[0].rstrip().split()
    kaupungit = int(rivi[0])
    verkko = nollaverkko(kaupungit)
    for i in range(1, len(lista) - 1):
        rivi = lista[i].rstrip().split()
        verkko[int(rivi[0]) - 1][int(rivi[1]) - 1] = int(rivi[2])
        verkko[int(rivi[1]) - 1][int(rivi[0]) - 1] = int(rivi[2])
    return verkko

def find_high(list):
    high = 0
    node = 0
    deadend = True
    for index, i in enumerate(list):
        if i > high:
            high = i
            node = index
            deadend = False
    if deadend:
        return 0, 0
    return high, node

def empty(list):
    for i in list:
        if i != 0:
            return False
    return True

def find_route(graph, goal):
    goal -= 1
    que = []
    que.append(graph[0])
    route = [1]
    done = False
    while len(que) != 0 and not done:
        node = que[-1]
        if route[-1] == (goal + 1):
            done = True
        elif empty(node):
            que.pop()
            route.pop()
        else:
            cost, nextNode = find_high(node)
            if cost > 0:
                node[nextNode] = 0
                que.pop()
                que.append(node)
                que.append(graph[nextNode])
                route.append(nextNode + 1)
            else:
                que.pop()
                route.pop()
    return route

def modified(graph, original):
    line = original[0].rstrip().split()
    cities = int(line[0])
    newGraph = nollaverkko(cities)
    goal = original[len(original) - 1]
    for i in range(0, len(graph)):
        rivi = graph[i].rstrip().split()
        newGraph[int(rivi[0]) - 1][int(rivi[1]) - 1] = int(rivi[2])
    return newGraph, goal

def find_highest(list, graph):
    high = 0
    for i in range(0, len(list) - 1):
        if graph[list[i] - 1][list[i + 1] - 1] > high:
            high = graph[list[i] - 1][list[i + 1] - 1]
    return high

def main():
    with open("./graph_large_testdata/graph_ADS2018_2000.txt", "r") as kohde:
        lista = kohde.readlines()
        kohde.close()
    cities = lista[0].rstrip().split()[0]
    g = Graph(int(cities))
    g.graph = muodosta_verkko(lista)
    g.primMST()
    with open("./temp.txt", "r") as target:
        new = target.readlines()
        target.close()
    newGraph, goal = modified(new, lista)
    highGraph = []
    for i in newGraph:
        highGraph.append(i.copy())
    route = find_route(newGraph, int(goal))
    high = find_highest(route, highGraph)
    print("Best route: {}".format(route))
    print("Highest point: {}".format(high))
    os.remove("temp.txt")

if __name__ == "__main__":
    main()
