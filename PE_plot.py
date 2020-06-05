import math
import time
import numpy as np
import random
import matplotlib.pyplot as plt 
import matplotlib
from collections import OrderedDict

npe = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H'] #Textbook example problem
# npe = [2,5,'V',1,'H',7,3,4,'V','H',6,'V',8,'V','H'] #M1
# npe = [2,5,'V',1,'H',7,3,4,'V','H','V',6,8,'H','V'] #M2 
# npe = [2,5,'V',1,'H',7,3,4,'V','H',6,'V',8,'H','V'] #M3
width = [2, 1, 3, 3, 3, 5, 1, 2]
height = [4, 3, 3, 5, 2, 3, 2, 4]

# npe = [4,3,5,'H',1,'V',6,7,'V','H',2,'V',8,'H','V']
# width = [5, 2, 6, 2, 6, 5, 3, 6]
# height = [3, 3, 3, 5, 2, 1, 8, 3]

# npe = [1,2,'H',3,4,'H',5,'H','V']
# width = [4, 4, 3, 4, 3]
# height = [6, 4, 4, 4, 4]

new_width = width[:]
new_height = height[:]
node = list(range(1,len(width)+1)) 
N = len(node)

def printNPE(s):
    for i in range(len(s)):
        print(s[i]),  #end =" ")
  
    print("")

def simulatedAnnealing(s):
    s_best = s[:]
    s_temp = s[:]
    T = 10000.0
    tic = time.clock()
    N_iter = 5*N

    while (T > 0.01):
        totm = 0
        reject = 0
        uphill = 0
        
        while (uphill < N_iter and totm <= 2*N_iter): 

            old_cost = area(s_temp)[0]

            b = random.randint(1,3)

            if b == 1:
                M1(s_temp)
            elif b == 2:
                M2(s_temp)
            elif b == 3:
                M3(s_temp)

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
        
        T = 0.99 * T

        if (float(reject/totm) > 0.95):
            break
    
    time_taken = time.clock() - tic
    s = s_best[:]
    print("Final: "),
    print(s)
    print("Area  : "),
    print(area(s)[0])
    print("Time: "),
    print(time_taken)
    plotRectangles(s)


def M1(s):
    A = []      
    for i in range(len(s)):
        if(s[i]!='V' and s[i]!='H'):  
            A.append(i)
    r = random.randint(0,len(A)-2)
    s[A[r]], s[A[r+1]] = s[A[r+1]], s[A[r]] 
    # print("After M1: "),
    # printNPE(s)
    # area(s)
    # print("--------------------------------------------------------------------")

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

    # print("After M2: "),
    # printNPE(s)
    # area(s)
    # print("--------------------------------------------------------------------")

def M3(s):
    A = []
    for i in range(len(s)-1):
        if((s[i]!='V' and s[i]!='H') and (s[i+1]=='H' or s[i+1]=='V')):
            A.append(i)

    while (True):
        r = random.randint(0,len(A)-1)
        k = A[r]   
        s[k+1], s[k] = s[k], s[k+1]
        if ((checkBallot(s) and checkSkewed(s)) is True):
            break

    # print("After M3: "),
    # printNPE(s)
    # area(s)
    # print("--------------------------------------------------------------------")

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
    
    # print("module",module)
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
    s1 = s[:]
    _,new_width,new_height, module = area(s1)
    
    x, y = getXY(new_width, new_height, module)
    co=['orange','green','yellow','pink','red','purple','gray','blue']

    _, ax = plt.subplots(1) 

    for i in range(N):
        rect= matplotlib.patches.Rectangle((x[i],y[i]), new_width[i], new_height[i], facecolor =co[i], linewidth=2.0) 
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

    return final_area, final_width, final_height, module


print("\nInitial : "), 
printNPE(npe)
final_area = area(npe)[0]
print("Area  : "),
print(final_area)
print("--------------------------------------------------------------------")
plotRectangles(npe)

simulatedAnnealing(npe)
# M1(npe)
# M2(npe)
# M3(npe)
