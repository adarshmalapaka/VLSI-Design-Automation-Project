from __future__ import print_function
import numpy as np
import itertools

user_input = raw_input("Enter the benchmark file for which Adjacency Matrix has to be generated = ")
netlist_file = open(user_input, mode = 'r')
node_netlist_file = open('Node_Netlist_Mapping', mode = 'w')

nodes = 0
node_list = []
for line in netlist_file:
    node_add = []
    if "#" not in line and line != "\n":
        if "DFF" in line or "AND" in line or "NAND" in line or "OR" in line or "NOR" in line or "NOT" in line or "XOR" in line or "XNOR" in line:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            a = line.split("=")
            node_add.append(nodes)
            nodes += 1
            node_add.append(a[0])
            a = a[1].split("(")
            a[1] = a[1].replace(')','')
            node_add.append(a[1])
            print("NODE =", node_add[0], ",TYPE =", a[0], ",OUTPUT =", node_add[1], ",INPUT =", node_add[2], file = node_netlist_file )
            node_list.append(node_add)
        else:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            line = line.replace(')', '')
            a = line.split('(')
            node_list.append(a)
            print(a[0] , a[1], file = node_netlist_file)
adjacency_list_netlist = np.zeros((nodes,nodes))

for i in node_list:
    if 'INPUT' in i or 'OUTPUT' in i:
        shorted_input = []
        if i[0] == 'INPUT':
            for k in node_list:
                if k[0] == "INPUT" or k[0] == "OUTPUT":
                    continue
                elif i[1] in k[2].split(','):
                    shorted_input.append(k[0])
            shorted_input = list(itertools.combinations(shorted_input,2))
            for k in shorted_input:
                adjacency_list_netlist[k[0]][k[1]] = 1
                adjacency_list_netlist[k[1]][k[0]] = 1

    else:
        for k in node_list:
            if k[0] == "INPUT" or k[0] == "OUTPUT":
                continue
            elif i[1] in k[2].split(','):
                adjacency_list_netlist[i[0]][k[0]] = 1
                adjacency_list_netlist[k[0]][i[0]] = 1

input_file = open('Input.txt' , mode = 'w')
for i in range(0,nodes):
    for j in range(0,nodes):
        print(int(adjacency_list_netlist[i][j]), end = ' ', file = input_file)
    print('\n', end = '', file = input_file)

