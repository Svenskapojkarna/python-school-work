# Tietorakenteet ja Algoritmit lopputyo
# Aleksi Hytonen, 2462633

import sys          # Needed for maxsize
import os           # Needed to remove the temporary file
import timeit       # Needed to show execution time

# Class Graph to contain the graph and make the Minimum spanning tree
class Graph(): 

    # Class constructor
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = [[0 for column in range(vertices)] 
                        for row in range(vertices)] 

    # Method to find the minimum key
    def minKey(self, key, mstSet): 
        min = sys.maxsize 

        for v in range(self.V): 
            if key[v] < min and mstSet[v] == False: 
                min = key[v] 
                min_index = v 

        return min_index

    # Method to save the minimum spanning tree to text file similarly to test data text files
    def printMST(self, parent): 
        f = open("temp.txt","w")
        for i in range(1, self.V):
            f.write("{} {} {}\n".format(parent[i] + 1, i + 1, self.graph[i][ parent[i] ]))
        f.close()

    # Function to construct minimum spanning tree using Prim's minimum spanning tree algorithm
    def primMST(self):  
        key = [sys.maxsize] * self.V 
        parent = [None] * self.V
        key[0] = 0
        mstSet = [False] * self.V 
        parent[0] = -1
        for i in range(self.V): 
            u = self.minKey(key, mstSet) 
            mstSet[u] = True
            for v in range(self.V): 
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]: 
                        key[v] = self.graph[u][v] 
                        parent[v] = u 
        self.printMST(parent) 

# Function to create a graph full of zeroes to be used in creating the graph from text file
# Par:      length = Int
# Return:   zero = Matrix (Array of arrays)
def zerograph(length):
    zero = []
    line = []
    for i in range(0, length):
        for j in range(0, length):
            line.append(0)
        zero.append(line)
        line = []
    return zero

# Function to create the graph from the text file
# Par:      list = Text from the text file
# return:   graph = Matrix (Array of arrays)
def make_graph(list):
    line = list[0].rstrip().split()
    cities = int(line[0])
    graph = zerograph(cities)
    for i in range(1, len(list) - 1):
        line = list[i].rstrip().split()
        graph[int(line[0]) - 1][int(line[1]) - 1] = int(line[2])
        graph[int(line[1]) - 1][int(line[0]) - 1] = int(line[2])
    return graph

# Function to find the highes weight of the next node and what is the index of that node
# Par:      list = array of Ints
# Return:   high = Int
#           node = Int
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

# Function to check if the node has unvisited neighbours
# Par:      list = array of ints
# Return:   False if node has unvisited neighbours, true if doesn't have
def empty(list):
    for i in list:
        if i != 0:
            return False
    return True

# Function to find the best route from MST of the original graph
# Par:      graph = Matrix (array of arrays)
#           goal = int
# Return:   route = array of ints
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

# Function to create a new graph from text file generated from MST
# Par:      graph = Matrix (array of arrays)
#           original = Matrix (array of arrays)
# Return:   newGraph = Matrix (array of arrays)
#           goal = int
def modified(graph, original):
    line = original[0].rstrip().split()
    cities = int(line[0])
    newGraph = zerograph(cities)
    goal = original[len(original) - 1]
    for i in range(0, len(graph)):
        line = graph[i].rstrip().split()
        newGraph[int(line[0]) - 1][int(line[1]) - 1] = int(line[2])
    return newGraph, goal

# Function to find the highest road between the best path cities
# Par:      list = array of ints
#           graph = Matrix (array of arrays)
# Return:   high = int
def find_highest(list, graph):
    high = 0
    for i in range(0, len(list) - 1):
        if graph[list[i] - 1][list[i + 1] - 1] > high:
            high = graph[list[i] - 1][list[i + 1] - 1]
    return high

# Main function. Steps taken during the execution:
# Step 1: Read the text file.
# Step 2: Read the amount of cities.
# Step 3: Generate the graph and prepare it for generating minimun spanning tree.
# Step 4: Read the new text file from generation of minimum spanning tree.
# Step 5: Create a new graph to be used in route generation.
# Step 6: Copy the graph so it can be used in calculation of highest road.
# Step 7: Calculate the best route.
# Step 8: Calculate the highest road.
# Step 9: Print the results.
# Step 10: Delete the temporary text file generated at step 3.
def main():
    start = timeit.default_timer()
    with open("./graph_large_testdata/graph_ADS2018_2000.txt", "r") as target:
        text = target.readlines()
        target.close()
    cities = text[0].rstrip().split()[0]
    g = Graph(int(cities))
    g.graph = make_graph(text)
    g.primMST()
    with open("./temp.txt", "r") as target:
        new = target.readlines()
        target.close()
    newGraph, goal = modified(new, text)
    highGraph = []
    for i in newGraph:
        highGraph.append(i[:])
    route = find_route(newGraph, int(goal))
    high = find_highest(route, highGraph)
    print("Best route: {}".format(route))
    print("Highest point: {}".format(high))
    os.remove("temp.txt")
    stop = timeit.default_timer()
    print('Time: ', stop - start)  

if __name__ == "__main__":
    main()
