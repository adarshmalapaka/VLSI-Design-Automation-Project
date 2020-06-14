import sys
import time
import sys
import numpy as np
import random
import matplotlib.pyplot as plt 
import matplotlib
from collections import OrderedDict


global N 
global node
global width
global height
global new_width
global new_height
lamda = 50

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


def parse_cell(parsed_data, adj):
    global width
    global height
    cell_dict = {}
    width = []
    height = []

    for i in range(len(parsed_data)):
        data = parsed_data[i]
        if data.find("AND")!=-1:
            if parsed_data[i][data.find("AND")-1]!='N':
                gate = "AND"
                w = 4
                h = 3
                colour = 'green'
            else:
                gate = "NAND"
                w = 6
                h = 4
                colour = 'red'
        if data.find("OR")!=-1:
            if parsed_data[i][data.find("OR")-1]!='N':
                gate = "OR"
                w = 5
                h = 4
                colour = 'purple'
            else:
                gate = "NOR"
                w = 6
                h = 5
                colour = 'blue'
        if data.find("NOT")!=-1:
            gate = "NOT"
            w = 3
            h = 2
            colour = 'pink'
        if data.find("DFF")!=-1:
            gate = "DFF"
            w = 8
            h = 5
            colour = 'yellow'

        temp = data.split(" ")[0]
        width.append(w)
        height.append(h)
        cell_dict[i+1] = temp, gate, w, h, colour

    return cell_dict, width, height

def parse_nodes(parsed_data):
    
    nodes = {}  
    for i in range(len(parsed_data)):
        temp = parsed_data[i].split(" ")[0]
        nodes[i] = temp

    return nodes

def generate_adjacency_matrix(isc_data, nodes):
    
    adjacency_matrix = [[0 for i in range(len(isc_data))] for j in range(len(isc_data))] 

    for k in range(len(isc_data)):
        for m in range(len(isc_data)):        
            if((nodes[k] in isc_data[m]) and (k!=m)):  
                adjacency_matrix[k][m]+=1 
                adjacency_matrix[m][k]+=1 

    return adjacency_matrix

def generateNPE(cell_dict,order):

    N = 133
    npe = []
    for i in range(1, N/16):
        npe.append(str(i))
    for i in range(0, (N/16)-2):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N/16, N/8):
        npe.append(str(i))
    for i in range(N/16, N/8):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")

    for i in range(N/8, N*3/16):
        npe.append(str(i))
    for i in range(N/8, (N*3/16)-1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N*3/16, N/4):
        npe.append(str(i))
    for i in range(N*3/16, (N/4)+1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")

    for i in range(N/4, N*5/16):
        npe.append(str(i))
    for i in range(N/4, (N*5/16)-1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N*5/16, N*3/8):
        npe.append(str(i))
    for i in range(N*5/16, N*3/8):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")

    for i in range(N*3/8, N*7/16):
        npe.append(str(i))
    for i in range(N*3/8, (N*7/16)-1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N*7/16, N/2):
        npe.append(str(i))
    for i in range(N*7/16, (N/2) + 2):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")

    for i in range(N/2, N*9/16):
        npe.append(str(i))
    for i in range(N/2, (N*9/16)-1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N*9/16, N*5/8):
        npe.append(str(i))
    for i in range(N*9/16, N*5/8):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")

    for i in range(N*5/8, N*11/16):
        npe.append(str(i))
    for i in range(N*5/8, (N*11/16)-1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N*11/16, N*3/4):
        npe.append(str(i))
    for i in range(N*11/16, (N*3/4)+1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")

    for i in range(N*3/4, N*13/16):
        npe.append(str(i))
    for i in range(N*3/4, (N*13/16)-1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N*13/16, N*7/8):
        npe.append(str(i))
    for i in range(N*13/16, N*7/8):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")

    for i in range(N*7/8, N*15/16):
        npe.append(str(i))
    for i in range(N*7/8, (N*15/16)-1):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    for i in range(N*15/16, N+1):
        npe.append(str(i))
    for i in range(N*15/16, N + 4):
        if random.uniform(0, 1) < 0.5:
            npe.append("V")
        else:
            npe.append("H")
    
    return npe



def printNPE(s):
    for i in range(len(s)):
        print(s[i]),
  
    print("")


def initialTemp(s,adj):
    P = 0.99
    s_temp = s[:]
    i = 0 
    k = 0 # number of uphill moves
    cost = 0.0
    old_cost = area(s_temp,adj)[4]
    while(i<N):
        delta = 0
        b = random.randint(1,3)
        if b == 1:
            M1(s_temp)
        elif b == 2:
            M2(s_temp)
        elif b == 3:
            M3(s_temp)

        new_cost = area(s_temp,adj)[4]
        delta = new_cost - old_cost
                
        if (delta > 0):
            old_cost = new_cost
            cost += delta
            k += 1
        
        i += 1

    avg_cost = cost/k 
    T0 = -avg_cost/np.log(P)
    if (T0 > 10000.0):
        T0 = 10000.0
    print("Initial Temperature: " + str(T0))
    return T0


def simulatedAnnealing(s,cell_dict,adj):
    global N
    s_best = s[:]
    s_temp = s[:]
    T0 = initialTemp(s,adj)
    tic = time.clock()
    N_iter = 2*N
    T = T0
    print("\n..... RUNNING SIMULATED ANNEALING PLACEMENT .....\n")
    while (T > 0.01):
        print("Completion %: "),
        print '{0}\r'.format(100 - np.interp(T,[0.01,T0],[0,100])),
        sys.stdout.flush()
        totm = 0
        reject = 0
        uphill = 0

        while (uphill < N_iter and totm <= N_iter): 

            old_cost = area(s_temp,adj)[4]
            b = random.randint(1,3)

            if b == 1:
                M1(s_temp)
            elif b == 2:
                M2(s_temp)
            elif b == 3:
                M3(s_temp)

            totm += 1
            new_cost = area(s_temp,adj)[4]
            delta = new_cost - old_cost
            r = np.random.random()

            if (delta<0 or (r<np.exp(-delta/T))):
                
                if (delta > 0):
                    uphill += 1

                s = s_temp[:]

                if (new_cost<area(s_best,adj)[4]):
                    s_best = s[:]

            else:
                reject += 1

        T = 0.99 * T

        if (float(reject/totm) > 0.90):
            break
    
    time_taken = time.clock() - tic
    s = s_best[:]
    final_area,_ ,_ ,_, final_cost = area(s,adj)

    min_dim = [area(s,adj)[1][(2*N)-1-1], area(s,adj)[2][(2*N)-1-1]]
    np.save("min_dim2", np.array(min_dim))
    
    return s, final_area, final_cost, time_taken


def M1(s):
    A = []      
    for i in range(len(s)):
        if(s[i]!='V' and s[i]!='H'):  
            A.append(i)
    r = random.randint(0,len(A)-2)
    s[A[r]], s[A[r+1]] = s[A[r+1]], s[A[r]] 


def M2(s):
    A = []   
    for i in range(len(s)-1):
        if ((s[i]!='V' and s[i]!='H') and (s[i+1]=='H' or s[i+1]=='V')):
            A.append(i+1)
    r = random.randint(0,len(A)-1)
    k = A[r]

    while (k < len(s)):
        if (s[k]=='H' or s[k]=='V'):
            if (s[k] is 'H'):
                s[k] = 'V'
            else:
                s[k] = 'H'
            k += 1
        else:
            break
    

def M3(s):
    A = []
    for i in range(len(s)-1):
        if((s[i]!='V' and s[i]!='H') and (s[i+1]=='H' or s[i+1]=='V')):
            A.append(i)

    r = random.randint(0,len(A)-1)
    k = A[r]   
    s[k+1], s[k] = s[k], s[k+1]

    if ((checkBallot(s) and checkSkewed(s)) is True):
        return True

    s[k], s[k+1] = s[k+1], s[k]
    return False


def checkBallot(s):

    a = 0
    b = 0
    for i in range(len(s)):
        if (s[i]=='H' or s[i]=='V'):
            a += 1
        if (s[i]!='V' and s[i]!='H'):
            b += 1
        if (a >= b):
            return False

    return True

def checkSkewed(s):
    for i in range(1,len(s)):
        if (s[i]=='H' or s[i]=='V'):
            j = s[i]
            if (s[i-1]==j):
                return False

    return True


def getXY(new_width, new_height, module):

    dn = []
    x = list(np.zeros(len(new_width)+1))
    y = list(np.zeros(len(new_height)+1))
    
    keys = []
    for key,_ in module.iteritems():
        keys.append(key)

    for i in reversed(keys):
        if (i not in dn):
            dn.append(i)

        for j in range(2):
            if (module[i][j] not in dn):

                if module[i][2]=='H':
                    #abH -> a/b with 'b' as reference

                    # xb,yb = xkey,ykey
                    x[module[i][1]-1] = x[i-1] 
                    y[module[i][1]-1] = y[i-1]
                    # xa,ya = xb,yb + (xb,hb)
                    x[module[i][0]-1] = x[module[i][1]-1]
                    y[module[i][0]-1] = y[module[i][1]-1] + new_height[module[i][1]-1] 


                    if (module[i][1] not in dn and module[i][j] not in dn):
                        dn.append(module[i][1])
                        dn.append(module[i][0])

                elif module[i][2]=='V':
                    # abV -> a|b with 'a' as reference
                    
                    # xa,ya = xkey,ykey
                    x[module[i][0]-1] = x[i-1] 
                    y[module[i][0]-1] = y[i-1]
                    # xb,yb = xa,ya + (wa,ya)
                    x[module[i][1]-1] = x[module[i][0]-1] + new_width[module[i][0]-1]
                    y[module[i][1]-1] = y[module[i][0]-1]  
          

                    if (module[i][0] not in dn and module[i][j] not in dn):
                        dn.append(module[i][0])
                        dn.append(module[i][1])

    return x, y


def plotPlacement(s,cell_dict,adj):
    global N
    s1 = s[:]
    _,new_width,new_height, module,_ = area(s1,adj)
    
    x_offset = 10
    y_offset = 10
    x, y = getXY(new_width, new_height, module)
    _, ax = plt.subplots(1) 

    coordinates = []
    dimensions = []
    center = []
    dim = []
    print("..... GENERATING PLOT .....\n")
    for i in range(N):
        x[i] = (x[i]*3) + 10
        y[i] = (y[i]*3) + 10
        
        x_center = x[i]+new_width[i]/2.0
        y_center = y[i]+new_height[i]/2.0
        center = [x_center, y_center]
        dim = [new_width[i], new_height[i]]
        coordinates.append(center)
        dimensions.append(dim)

        rect= matplotlib.patches.Rectangle((x[i],y[i]), new_width[i], new_height[i], facecolor =cell_dict[i+1][4], linewidth=2.0) 
        plt.text(x_center,y_center,str(i+1))
        ax.add_patch(rect) 

    max_x = max(x)+max(width)+10
    max_y = max(y)+max(height)+10
    plt.xlim([0, max_x])
    plt.ylim([0, max_y])
    plt.xticks(np.arange(0, max_x, 5.0))
    plt.yticks(np.arange(0, max_y, 5.0))
    
    plt.title('Final Placement', fontsize = 32)
    plt.grid()   
    plt.show() 

    np.save("coordinates2", np.array(coordinates))
    np.save("dimensions2", np.array(dimensions))


def newDimensions(w1,h1,w2,h2,hv):
    if hv=='H':
        width.append(max(w1,w2))
        height.append(h1 + h2)
    elif hv=='V':
        width.append(w1 + w2)
        height.append(max(h1,h2))


def area(s,adj):
    s1 = s[:]
    module = OrderedDict() 
    # Note: Regular Python dictionary is unordered and hence does not necessarily store 
    # newly added key-value pairs in sequence, hence use OrderedDict() 

    for i in range(2,N+1):
        try:
            find_H = s1.index('H')
        except:
            find_H = 100000
        try:
            find_V = s1.index('V')
        except:
            find_V = 100000
        
        q = find_H if find_H < find_V else find_V

        if(len(s1)>=3):
            node.append(len(node)+1)
            module[node[len(node)-1]] = (int(s1[q-2]), int(s1[q-1]), s1[q])
            newDimensions(width[int(s1[q-2])-1],height[int(s1[q-2])-1],width[int(s1[q-1])-1],height[int(s1[q-1])-1],s1[q])
            s1.pop(q) and s1.pop(q-1) and s1.pop(q-2)
            s1.insert(q-2,node[len(node)-1])

    final_width = width[:]
    final_height = height[:] 

    final_area = final_width[len(width)-1] * final_height[len(height)-1]

    for i in range(2,N+1):
        width.pop(len(height)-1)
        height.pop(len(height)-1)
        node.pop(len(node)-1)

    WL = max(final_width) + max(final_height)
    cost = final_area + lamda*WL # Cost = Area + Lamda * WL
    
    return final_area, final_width, final_height, module, cost


def main():

    if(len(sys.argv) == 2):
            
        isc_filename = str(sys.argv[1])
        isc_data = read_isc_file(isc_filename)
        parsed_data = parse_isc_data(isc_data)

        nodes = parse_nodes(parsed_data)
        print("\n..... NODES PARSED FROM ISCAS NETLIST .....\n")

        adj = generate_adjacency_matrix(parsed_data, nodes)
        print("..... ADJACENCY MATRIX GENERATED, " + str(len(adj)) + " x " + str(len(adj[0])) + " Matrix ..... \n")
        
        global N
        global node
        global width
        global height
        global new_width
        global new_height
        global X
        global Y
        
        cell_dict, width, height = parse_cell(parsed_data, adj)
        new_width = width[:]
        new_height = height[:]
        npe = generateNPE(cell_dict,'H')
        print("***** INITIAL POLISH EXPRESSION GENERATED *****\n")

        N = len(cell_dict)
        node = list(range(1,N+1))
          
        initial_area,_ ,_ ,_, initial_cost = area(npe,adj)
      
        new_npe, final_area, final_cost, time_taken = simulatedAnnealing(npe,cell_dict,adj)
        plotPlacement(new_npe,cell_dict,adj)
        print("***** RESULTS *****\n")
        print("Initial Area  : " + str(initial_area))
        print("Initial Cost  : " + str(initial_cost))
        print("Final Area  : " + str(initial_area))
        print("Final Cost  : " + str(initial_cost))
        
        print("Initial PE: "), 
        printNPE(npe)
        print("Final PE: "), 
        printNPE(new_npe)

    else:
        print("ERROR: Incorrect number of arguments!")
        print("USAGE: python floorplan_placement.py <ISC_FILENAME>")
        print("       ISC_FILENAME - For ex: s298.isc")
        exit(0) 


if __name__ == "__main__":
    main()
