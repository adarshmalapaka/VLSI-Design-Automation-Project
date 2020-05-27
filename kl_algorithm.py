import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
import random


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
                
def kl_partition(adj, nodes, random_order=0):
    
    print("\n..... RUNNING KERNIGHAN LIN ALGORITHM .....\n")

    initial_time = time.process_time()
    part = list(range(0,len(nodes)))
    
    if random_order == '1':
        random.shuffle(part)
        print("..... RANDOMIZING INITIAL PARTITIONS .....\n")

    initial_partition = (part[:len(part)//2], part[len(part)//2:])

    names_A = node_mapping(initial_partition[0], nodes)
    names_B = node_mapping(initial_partition[1], nodes)
    
    print("***** INITIAL PARTITIONS *****\n")
    print("Partition A: " + str(names_A))
    print("\n")
    print("Partition B: " + str(names_B))
    print("\n")

    G = nx.from_numpy_matrix(np.array(adj), parallel_edges=True, create_using=nx.MultiGraph()) 
    partition = nx.algorithms.community.kernighan_lin_bisection(G, partition=initial_partition)

    initial_cut_size = 0
    edge = list(G.edges())
 
    for i in range(len(edge)):
        if edge[i][0] in initial_partition[0] and edge[i][1] in initial_partition[1]:
            initial_cut_size += 1

        elif edge[i][0] in initial_partition[1] and edge[i][1] in initial_partition[0]:
            initial_cut_size += 1


    final_cut_size = 0
    for i in range(len(edge)):
        if edge[i][0] in partition[0] and edge[i][1] in partition[1]:
            final_cut_size += 1

        elif edge[i][0] in partition[1] and edge[i][1] in partition[0]:
            final_cut_size += 1

    time_taken = time.process_time() - initial_time
    generate_plot(G, initial_partition, 1, nodes)

    return partition, G, initial_cut_size, final_cut_size, time_taken

def generate_plot(G, partition, fig_num, nodes):

    print("..... GENERATING PLOT .....\n")

    pos_A = nx.circular_layout(partition[0])
    pos_B = nx.circular_layout(partition[1])
    pos = {}
    pos.update(pos_A)
    pos.update(pos_B)

    for i in range(len(pos)):
        if i in partition[1]:
            pos[i][0] += 5.0

    node_colors_map = {}
    for i, lg in enumerate(partition):
        for node in lg:
            node_colors_map[node] = i
    node_colors = [node_colors_map[n] for n in G.nodes]
    
    plt.figure(num=fig_num,figsize=(20,10))
    plt.axis("off")
    if fig_num is 1:
        plt.title('Initial Partitions - KL Algorithm', fontsize = 32)
    elif fig_num is 2:
        plt.title('Final Partitions - KL Algorithm', fontsize = 32)
    nx.draw_networkx(G, pos=pos, node_size=250, with_labels=True, cmap=plt.cm.cool, node_color=node_colors, labels=nodes)
    # plt.savefig("fig_kl"+str(fig_num)+".png", dpi=1200)
    plt.show()

def main():

    if(len(sys.argv) == 3):
            
        isc_filename = str(sys.argv[1])
        isc_data = read_isc_file(isc_filename)
        parsed_data = parse_isc_data(isc_data)

        nodes = parse_nodes(parsed_data)

        print("\n..... NODES PARSED FROM ISCAS NETLIST .....\n")
        
        adj = generate_adjacency_matrix(parsed_data, nodes)
        print("..... ADJACENCY MATRIX GENERATED, " + str(len(adj)) + " x " + str(len(adj[0])) + " Matrix ..... \n")

        random_order = str(sys.argv[2])
        [partition, G, initial_cut_size, final_cut_size, time_taken] = kl_partition(adj, nodes, random_order)

        names_A = node_mapping(partition[0], nodes)
        names_B = node_mapping(partition[1], nodes)

        print("***** FINAL PARTITIONS *****\n")
        print("Partition A: " +  str(names_A))
        print('\n')
        print("Partition B: " + str(names_B))
        print("\n")
        
        
        print("***** RESULTS *****\n")
        print("Total time taken (in seconds): " + str(time_taken))
        print("Initial Cut Size: " + str(initial_cut_size))
        print("Minimum Cut Size: " + str(final_cut_size))
        print("\n")

        generate_plot(G, partition, 2, nodes)
            
    else:
        print("ERROR: Incorrect number of arguments!")
        print("USAGE: python kl_algorithm.py <ISC_FILENAME> <RANDOM>")
        print("       ISC_FILENAME - For ex: s298.isc")
        print("       RANDOM       - 1 for random initial partition")
        print("                      0 for normal initial partition")
        exit(0) 


if __name__ == "__main__":
    main()
    