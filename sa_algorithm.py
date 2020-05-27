import sys
import networkx as nx
import matplotlib.pyplot as plt 
import random
import math
import numpy as np
import time

       
Infinity = 10000
Alpha = 0.999
Threshold = 5000


def read_isc_file(filename):
   
    with open(filename) as f:
        isc_data = list(f)
    f.close()
    return isc_data


def parse_isc_data(isc_data):
    
    parsed_data = []

    for i in range(len(isc_data)):
        temp = isc_data[i].split("#")[0].split("\n")[0].split("INPUT")[0].split("OUTPUT")[0]
        
        if temp != '':
            parsed_data.append(temp)

    for i in range(len(parsed_data)):

        if "G10" in parsed_data[i]:
            if "G10 " in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G10 ","Ga ")
            elif "G10," in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G10,","Ga,")
            elif "G10)" in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G10)","Ga)")
        
        if "G11" in parsed_data[i]:
            if "G11 " in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G11 ","Gb ")
            elif "G11," in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G11,","Gb,")
            elif "G11)" in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G11)","Gb)")
        
        if "G12" in parsed_data[i]:
            if "G12 " in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G12 ","Gc ")
            elif "G12," in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G12,","Gc,")
            elif "G12)" in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G12)","Gc)")
        
        if "G13" in parsed_data[i]:
            if "G13 " in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G13 ","Gd ")
            elif "G13," in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G13,","Gd,")
            elif "G13)" in parsed_data[i]:
                parsed_data[i] = parsed_data[i].replace("G13)","Gd)")
            
    return parsed_data


def parse_nodes(parsed_data):
    
    nodes = {}  
    for i in range(len(parsed_data)):
        temp = parsed_data[i].split(" ")[0]
        nodes[i] = temp

    return nodes


def node_mapping(arr, nodes):

    node_map = []
    for i in arr:
        if nodes[i] == 'Ga':
            nodes[i] = 'G10'
        elif nodes[i] == 'Gb':
            nodes[i] = 'G11'
        elif nodes[i] == 'Gc':
            nodes[i] = 'G12'
        elif nodes[i] == 'Gd':
            nodes[i] = 'G13'

        node_map.append(nodes[i]) 

    return node_map


def generate_adjacency_matrix(isc_data, nodes):
    
    adjacency_matrix = [[0 for i in range(len(isc_data))] for j in range(len(isc_data))] 

    for k in range(len(isc_data)):
        for m in range(len(isc_data)):        
            if((nodes[k] in isc_data[m]) and (k!=m)):  
                adjacency_matrix[k][m]+=1 
                adjacency_matrix[m][k]+=1 

    return adjacency_matrix


def cutsize_cost(A, B, adj):

    cut_size = 0

    for i in A:
        for j in B:
            if(adj[i][j] == 1 or adj[j][i] == 1):
                    cut_size += 1
            elif(adj[i][j] > 1):
                    cut_size += adj[i][j]
            elif(adj[j][i] > 2):
                    cut_size += adj[j][i]

    return cut_size


def sa_partition(adj, nodes, random_order=0):
    
    print("\n..... RUNNING SIMULATED ANNEALING ALGORITHM .....\n")

    Temp = Infinity

    part = list(range(0,len(nodes)))
    
    if random_order == '1':
        random.shuffle(part)
        print("..... RANDOMIZING INITIAL PARTITIONS .....\n")

    A = part[:len(part)//2]
    B = part[len(part)//2:]

    number_cuts = []
    cut_ratio = []
    minCost = cutsize_cost(A,B,adj)

    names_A = node_mapping(A, nodes)
    names_B = node_mapping(B, nodes)
    
    number_cuts.append(minCost)

    print("***** INITIAL PARTITIONS *****\n")
    print("Partition A: " + str(names_A))
    print("\n")
    print("Partition B: " + str(names_B))
    print("\n")

    initial_time = time.process_time()

    while(Temp > Threshold):

        a = A
        b = B
	
        i = random.randint(0,len(A)-1)
        j = random.randint(0,len(B)-1)
        temp = a[i]
        a[i] = b[j]
        b[j] = temp
        cost = cutsize_cost(a, b, adj)
        number_cuts.append(cost)
        
        delta = cost - minCost
        
        if (delta<0):
            A = a
            B = b
            minCost = cost
        else:
            p = np.exp(-delta / Temp)
            if(np.random.random()<p):
                A = a
                B = b
                minCost = cost
        
        Temp *= Alpha 
       
    cut_ratio = np.true_divide(number_cuts, (len(A)*len(B))) 
    partition = (A,B)

    return partition, number_cuts, cut_ratio, initial_time,

def main():
         
    if(len(sys.argv) == 3):
        
        isc_filename = str(sys.argv[1])
        isc_data = read_isc_file(isc_filename)
        parsed_data = parse_isc_data(isc_data)

        nodes = parse_nodes(parsed_data)
        print("\n..... NODES PARSED FROM ISCAS NETLIST .....\n")

        adj = generate_adjacency_matrix(parsed_data, nodes)
        print("..... ADJACENCY MATRIX GENERATED, " + str(len(adj)) + " x " + str(len(adj[0])) + " Matrix ..... \n")

        print("***** PARAMETERS FOR SA ALGORITHM *****\n")
        print("Infinity: " + str(Infinity))
        print("Alpha: " + str(Alpha))
        print("Threshold: " + str(Threshold))
        print("Total Number of Nodes: " + str(len(adj)))
        
        random_order = str(sys.argv[2])
        partition, number_cuts, cut_ratio, initial_time = sa_partition(adj, nodes, random_order)
        
        names_A = node_mapping(partition[0], nodes)
        names_B = node_mapping(partition[1], nodes)
          
        print("***** FINAL PARTITIONS *****\n")
        print("Partition A: " +  str(names_A))
        print('\n')
        print("Partition B: " + str(names_B))
        print("\n")
        
        print("***** RESULTS *****\n")
        time_taken = time.process_time() - initial_time
        print("Total time taken (in seconds): " + str(time_taken))
        print("Initial Cut Size: " + str(number_cuts[0]))
        print("Minimum Cut Size: " + str(min(number_cuts)))
        print("\n")

        plt.figure()
        plt.xlabel("Iterations")
        plt.ylabel("Cut Cost (or) Cut Ratio ")
        plt.title('Cut Ratio per Iteration')
        plt.plot(cut_ratio)
        plt.show()
        
    else:
        print("ERROR: Incorrect number of arguments!")
        print("USAGE: python sa_algorithm.py <ISC_FILENAME> <RANDOM>")
        print("       ISC_FILENAME - For ex: s298.isc")
        print("       RANDOM       - 1 for random initial partition")
        print("                      0 for normal initial partition")
        exit(0) 

if __name__ == "__main__":
    main()