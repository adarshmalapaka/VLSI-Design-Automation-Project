import sys
import time
import sys
import numpy as np
import random
import matplotlib.pyplot as plt 
import matplotlib
from collections import OrderedDict


# npe = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H'] #Textbook example problem
# width = [2, 1, 3, 3, 3, 5, 1, 2]
# height = [4, 3, 3, 5, 2, 3, 2, 4]

# npe = [4,3,5,'H',1,'V',6,7,'V','H',2,'V',8,'H','V']
# width = [5, 2, 6, 2, 6, 5, 3, 6]
# height = [3, 3, 3, 5, 2, 1, 8, 3]

# npe = [1,2,'H',3,4,'H',5,'H','V']
# width = [4, 4, 3, 4, 3]
# height = [6, 4, 4, 4, 4]

# new_width = width[:]
# new_height = height[:]
# node = list(range(1,len(width)+1)) 
# N = len(node)
global N 
# global npe
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


def parse_cell(parsed_data):
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
            else:
                gate = "NAND"
                w = 6
                h = 4
        if data.find("OR")!=-1:
            if parsed_data[i][data.find("OR")-1]!='N':
                gate = "OR"
                w = 5
                h = 4
            else:
                gate = "NOR"
                w = 6
                h = 5
        if data.find("NOT")!=-1:
            gate = "NOT"
            w = 3
            h = 2
        if data.find("DFF")!=-1:
            gate = "DFF"
            w = 8
            h = 5

        temp = data.split(" ")[0]
        width.append(w)
        height.append(h)
        cell_dict[i+1] = temp, gate, w, h

    return cell_dict, width, height

def generateNPE(cell_dict,order):
    npe = []
    for key,_ in cell_dict.iteritems():
        npe.append(key)
        if key is 1:
            continue
        npe.append(order)
        order = 'H' if order is 'V' else 'V'
    return npe

def printNPE(s):
    for i in range(len(s)):
        print(s[i]),  #end =" ")
  
    print("")


def initialTemp(s):
    P = 0.99
    s_temp = s[:]
    i = 0 
    k = 0 # number of uphill moves
    cost = 0.0
    old_cost = area(s_temp)[4]

    while(i<N):
        delta = 0
        b = random.randint(1,3)
        if b == 1:
            M1(s_temp)
        elif b == 2:
            M2(s_temp)
        elif b == 3:
            if M3(s_temp) is False:
                M2(s_temp)

        new_cost = area(s_temp)[4]
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
    print("initial",T0)
    return T0


def simulatedAnnealing(s):
    global N
    s_best = s[:]
    s_temp = s[:]
    T0 = initialTemp(s)
    tic = time.clock()
    N_iter = 2*N
    T = T0
    while (T > 0.01):
        print("Percent: "),
        print '{0}\r'.format(100 - np.interp(T,[0.01,T0],[0,100]))
        totm = 0
        reject = 0
        uphill = 0

        while (uphill < N_iter and totm <= N_iter): 

            old_cost = area(s_temp)[0]

            b = random.randint(1,3)
            print(s)
            if b == 1:
                M1(s_temp)
            elif b == 2:
                M2(s_temp)
            elif b == 3:
                if M3(s_temp) is False:
                    M2(s_temp)
                    M1(s_temp)

            totm += 1
            new_cost = area(s_temp)[0]
            delta = new_cost - old_cost
            r = np.random.random()

            if (delta<0 or (r<np.exp(-delta/T))):
                
                if (delta > 0):
                    uphill += 1

                s = s_temp[:]

                if (area(s)[0]<area(s_best)[0]):
                    s_best = s[:]

            else:
                reject += 1

        # print(time.clock()-tic1)
        T = 0.99 * T
        # plotRectangles(s)
        if (float(reject/totm) > 0.90):# or (time.clock()-tic) > 40):
            break
    
    time_taken = time.clock() - tic
    print("plains",s)
    print("plains",area(s)[0])
    s = s_best[:]
    print("temp",s_temp)
    print("temp",area(s_temp)[0])
    print("Final: "),
    print(s)
    print("Area  : "),
    print(area(s)[0])
    print("Time: "),
    print(time_taken)
    plotRectangles(s)


# def simulatedAnnealing(s):

#     global N
#     s_best = s[:]
#     # s_temp = s[:]
#     T0 = initialTemp(s)#10000.0
#     tic = time.clock()
#     N_iter = 5*N
#     T = T0
#     while (T > 0.01):
#         print("Percent: "),
#         print '{0}\r'.format(100 - np.interp(T,[0.01,T0],[0,100]))
#         sys.stdout.flush()
#         # print(T)
#         totm = 0

#         while (totm <= 1*N_iter): 

#             old_cost = area(s)[4]

#             b = random.randint(1,3)
#             s_new = s[:]
#             if b == 1:
#                 M1(s_new)
#             elif b == 2:
#                 M2(s_new)
#             elif b == 3:
#                 if M3(s_new) is False:
#                     M2(s_new)
                    # M1(s_temp)

#             totm += 1
#             new_cost = area(s_new)[4]
#             delta = new_cost - old_cost
            
#             r = np.random.random()

#             if (delta<=0 or r<np.exp(-delta/T)): 
#                 s = s_new[:]

#             if (area(s_best)[4]>area(s)[4]):
#                     s_best = s[:]

#         # print(time.clock()-tic1)
#         T = 0.99 * T
#         print("Area",area(s_best)[0])
#         # print("")
#         # plotRectangles(s)


#     time_taken = time.clock() - tic
#     print("plains",s)
#     print("plains",area(s)[0])
#     s = s_best[:]
#     print("new",s_new)
#     print("new",area(s_new)[0])
#     print("Final: "),
#     print(s)
#     print("Area  : "),
#     print(area(s)[0])
#     print("Time: "),
#     print(time_taken)
#     plotRectangles(s)


def M1(s):
    # print("M1")
    A = []      
    for i in range(len(s)):
        if(s[i]!='V' and s[i]!='H'):  
            A.append(i)
    r = random.randint(0,len(A)-2)
    s[A[r]], s[A[r+1]] = s[A[r+1]], s[A[r]] 
    # print(s)
    # print("After M1: "),
    # printNPE(s)
    # area(s)
    # print("--------------------------------------------------------------------")

def M2(s):
    # print("M2")
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
    
    # print(s)
    # print("After M2: "),
    # printNPE(s)
    # area(s)
    # print("--------------------------------------------------------------------")

def M3(s):
    # print("M3")
    A = []
    for i in range(len(s)-1):
        if((s[i]!='V' and s[i]!='H') and (s[i+1]=='H' or s[i+1]=='V')):
            A.append(i)
    # print(A)
    # while (True):
    r = random.randint(0,len(A)-1)
    k = A[r]   
    # print("1",s[k+1], s[k])
    s[k+1], s[k] = s[k], s[k+1]
    # print("2",s[k-1], s[k])
    if ((checkBallot(s) and checkSkewed(s)) is True):
        print("break")
        # break
        # print(s)
        return True
    s[k], s[k+1] = s[k+1], s[k]
    return False
    # print(s)
    # print("After M3: "),
    # printNPE(s)
    # area(s)
    # print("--------------------------------------------------------------------")

def checkBallot(s):
    # print("Ballot")
    # print(s)
    a = 0
    b = 0
    for i in range(len(s)):
        if (s[i]=='H' or s[i]=='V'):
            a += 1
        if (s[i]!='V' and s[i]!='H'):
            b += 1
        if (a >= b):
            # print("False",a,b)
            return False
        # print(a,b)
    # print("EndBallot")

    return True

def checkSkewed(s):
    # print("Skewed")
    for i in range(1,len(s)):
        if (s[i]=='H' or s[i]=='V'):
            j = s[i]
            if (s[i-1]==j):
                return False
    # print("EndSkewed")
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
                # print(i,module[i][0],module[i][1],module[i][2])

                if module[i][2]=='H':
                    #abH -> a/b with 'b' as reference

                    # xb,yb = xkey,ykey
                    x[module[i][1]-1] = x[i-1] 
                    y[module[i][1]-1] = y[i-1]
                    # xa,ya = xb,yb + (xb,hb)
                    x[module[i][0]-1] = x[module[i][1]-1]
                    y[module[i][0]-1] = y[module[i][1]-1] + new_height[module[i][1]-1] 

                    # print(module[i][1])
                    # print(module[i][0])

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

                    # print(module[i][0])
                    # print(module[i][1])
                    
                    if (module[i][0] not in dn and module[i][j] not in dn):
                        dn.append(module[i][0])
                        dn.append(module[i][1])

    return x, y


def plotRectangles(s):
    global N
    s1 = s[:]
    _,new_width,new_height, module,_ = area(s1)
    
    x, y = getXY(new_width, new_height, module)
    co=['orange','green']

    _, ax = plt.subplots(1) 

    for i in range(N):
        rect= matplotlib.patches.Rectangle((x[i],y[i]), new_width[i], new_height[i], facecolor =co[0], linewidth=2.0) 
        plt.text(x[i]+new_width[i]/2.0,y[i]+new_height[i]/2.0,str(i+1))
        ax.add_patch(rect) 

    plt.xticks(np.arange(0, max(new_width[len(new_width)-1],new_height[len(new_height)-1])+1, 1.0))
    plt.yticks(np.arange(0, max(new_width[len(new_width)-1],new_height[len(new_height)-1])+1, 1.0))
    plt.grid()   
    plt.show() 


def newDimensions(w1,h1,w2,h2,hv):
    if hv=='H':
        width.append(max(w1,w2))
        height.append(h1 + h2)
    elif hv=='V':
        width.append(w1 + w2)
        height.append(max(h1,h2))


def area(s):
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

        # print(s1)
    # print(module)
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


# print("\nInitial : "), 
# printNPE(npe)
# final_area = area(npe)[0]
# print("Area  : "),
# print(final_area)
# print("--------------------------------------------------------------------")
# plotRectangles(npe)

# simulatedAnnealing(npe)
# M1(npe)
# M2(npe)
# M3(npe)


def main():

    if(len(sys.argv) == 2):
            
        isc_filename = str(sys.argv[1])
        isc_data = read_isc_file(isc_filename)
        # print(isc_data)
        # print("")
        parsed_data = parse_isc_data(isc_data)
        # print(parsed_data)
        # print("")
        
        global N
        # global npe
        global node
        global width
        global height
        global new_width
        global new_height
        cell_dict, width, height = parse_cell(parsed_data)
        new_width = width[:]
        new_height = height[:]
        npe = generateNPE(cell_dict,'H')
        # npe = [61, 19, 'H', 28, 'V', 14, 'V', 11, 'H', 13, 'V', 9, 'H', 51, 'H', 39, 'H', 26, 'V', 5, 'H', 57, 'H', 32, 'H', 17, 'V', 1, 'V', 52, 'V', 27, 'H', 3, 'V', 34, 'V', 112, 'H', 73, 'V', 37, 'V', 115, 'H', 7, 'H', 12, 'H', 102, 'V', 21, 'H', 20, 'V', 35, 'V', 16, 'V', 95, 'V', 77, 'V', 36, 'H', 79, 'V', 10, 'V', 119, 'H', 82, 'H', 42, 'V', 22, 'V', 83, 'V', 15, 'H', 105, 'H', 117, 'V', 23, 'H', 30, 'H', 74, 'V', 31, 'V', 6, 'H', 46, 'V', 33, 'V', 88, 'H', 62, 'H', 69, 'H', 25, 'H', 97, 'H', 40, 'H', 100, 'V', 81, 'V', 29, 'H', 54, 'H', 49, 'V', 94, 'V', 43, 'V', 120, 'V', 65, 'H', 64, 'H', 92, 'V', 127, 'V', 47, 'V', 85, 'H', 90, 'H', 44, 'H', 24, 'H', 68, 'H', 80, 'V', 101, 'V', 128, 'V', 118, 'V', 84, 'V', 129, 'V', 98, 'V', 55, 'V', 125, 'V', 76, 'H', 41, 'H', 66, 'V', 130, 'H', 86, 'H', 106, 'H', 103, 'H', 56, 'H', 8, 'H', 48, 'H', 50, 'H', 67, 'V', 93, 'H', 99, 'V', 124, 'H', 4, 'V', 63, 'H', 53, 'H', 123, 'V', 2, 'H', 38, 'V', 78, 'H', 96, 'H', 58, 'H', 18, 'H', 89, 'V', 107, 'H', 45, 'H', 59, 'V', 72, 'H', 75, 'V', 60, 'V', 111, 'H', 113, 'H', 114, 'H', 108, 'V', 131, 'H', 71, 'V', 121, 'H', 109, 'H', 104, 'H', 87, 'V', 133, 'V', 70, 'V', 91, 'V', 116, 'V', 110, 'V', 122, 'H', 132, 'H', 126, 'H']
        # temp = [61, 19, 'H', 28, 'V', 14, 'V', 11, 'H', 13, 'V', 9, 'H', 51, 'H', 39, 'H', 26, 'V', 5, 'H', 57, 'H', 32, 'H', 17, 'V', 1, 'V', 52, 'V', 27, 'H', 3, 'V', 34, 'V', 112, 'H', 73, 'V', 37, 'V', 115, 'H', 7, 'H', 12, 'H', 102, 'V', 21, 'H', 20, 'V', 35, 'V', 16, 'V', 95, 'V', 77, 'V', 36, 'H', 79, 'V', 10, 'V', 119, 'H', 82, 'H', 42, 'V', 22, 'V', 83, 'V', 15, 'H', 105, 'H', 117, 'V', 23, 'H', 30, 'H', 74, 'V', 31, 'V', 6, 'H', 46, 'V', 33, 'V', 88, 'H', 62, 'H', 69, 'H', 25, 'H', 97, 'H', 40, 'H', 100, 'V', 81, 'V', 29, 'H', 54, 'H', 49, 'V', 94, 'V', 43, 'V', 120, 'V', 65, 'H', 64, 'H', 92, 'V', 127, 'V', 47, 'V', 85, 'H', 90, 'H', 44, 'H', 24, 'H', 68, 'H', 80, 'V', 101, 'V', 128, 'V', 118, 'V', 84, 'V', 129, 'V', 98, 'V', 55, 'V', 125, 'V', 76, 'H', 41, 'H', 66, 'V', 130, 'H', 86, 'H', 106, 'H', 103, 'H', 56, 'H', 8, 'H', 48, 'H', 50, 'H', 67, 'V', 93, 'H', 99, 'V', 124, 'H', 4, 'V', 63, 'H', 53, 'H', 123, 'V', 2, 'H', 38, 'V', 78, 'H', 96, 'H', 58, 'H', 18, 'H', 89, 'V', 107, 'H', 45, 'H', 59, 'V', 72, 'H', 75, 'V', 60, 'V', 111, 'H', 113, 'H', 114, 'H', 108, 'V', 131, 'H', 71, 'V', 121, 'H', 109, 'H', 104, 'H', 87, 'V', 133, 'V', 70, 'V', 91, 'V', 116, 'V', 110, 'V', 122, 'H', 132, 'H', 126, 'H']
        # npe = [55, 15, 'H', 90, 'V', 45, 'H', 3, 'H', 64, 'H', 128, 'H', 74, 'H', 16, 'H', 47, 'H', 121, 'H', 46, 'H', 25, 'H', 111, 'H', 37, 'H', 32, 'H', 8, 'H', 87, 'H', 78, 'H', 52, 'H', 120, 'H', 129, 'H', 56, 'H', 61, 'H', 18, 'H', 7, 'H', 9, 'H', 2, 'V', 58, 'H', 95, 'H', 6, 'H', 44, 'H', 65, 'H', 40, 'H', 20, 'H', 110, 'H', 59, 'H', 73, 'H', 36, 'H', 12, 'H', 103, 'H', 30, 'H', 42, 'H', 51, 'H', 82, 'H', 109, 'H', 1, 'H', 13, 'H', 63, 'H', 126, 'H', 80, 'H', 70, 'H', 60, 'H', 85, 'H', 38, 'H', 91, 'H', 39, 'H', 19, 'H', 5, 'H', 4, 'H', 97, 'H', 89, 'H', 98, 'H', 117, 'H', 48, 'H', 11, 'H', 83, 'H', 77, 'H', 84, 'H', 68, 'H', 43, 'H', 26, 'H', 132, 'H', 21, 'H', 34, 'H', 81, 'H', 49, 'H', 133, 'H', 75, 'H', 104, 'H', 50, 'H', 28, 'H', 31, 'H', 29, 'H', 108, 'H', 54, 'H', 94, 'H', 107, 'H', 93, 'H', 119, 'H', 66, 'H', 67, 'H', 23, 'H', 112, 'H', 41, 'H', 114, 'H', 122, 'H', 14, 'H', 113, 'H', 79, 'H', 72, 'H', 86, 'H', 17, 'H', 102, 'H', 127, 'H', 69, 'H', 118, 'H', 105, 'H', 33, 'H', 125, 'H', 130, 'H', 88, 'H', 123, 'H', 96, 'H', 24, 'H', 76, 'H', 62, 'H', 92, 'H', 115, 'H', 131, 'H', 27, 'H', 10, 'H', 53, 'H', 106, 'H', 116, 'H', 101, 'H', 57, 'H', 100, 'H', 99, 'H', 35, 'H', 22, 'H', 124, 'H', 71, 'H']
        N = len(cell_dict)
        node = list(range(1,N+1))
        
        print("\nInitial : "), 
        printNPE(npe)
        final_area = area(npe)[0]
        print("Area  : "),
        print(final_area)
        print("--------------------------------------------------------------------")
        # plotRectangles(npe)

        # M3(npe)
        # printNPE(npe)
        simulatedAnnealing(npe)


        # print(nodes)
        # cell = parse_cell(parsed_data)
        # print("")

        # print("\n..... NODES PARSED FROM ISCAS NETLIST .....\n")
        
        # adj = generate_adjacency_matrix(parsed_data, nodes)
        # print("..... ADJACENCY MATRIX GENERATED, " + str(len(adj)) + " x " + str(len(adj[0])) + " Matrix ..... \n")

        # random_order = str(sys.argv[2])
        # [partition, G, initial_cut_size, final_cut_size, time_taken] = kl_partition(adj, nodes, random_order)

        # names_A = node_mapping(partition[0], nodes)
        # names_B = node_mapping(partition[1], nodes)

 

        # generate_plot(G, partition, 2, nodes)
            
    else:
        print("ERROR: Incorrect number of arguments!")
        print("USAGE: python kl_algorithm.py <ISC_FILENAME>")
        print("       ISC_FILENAME - For ex: s298.isc")
        exit(0) 


if __name__ == "__main__":
    main()


