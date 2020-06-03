import math
import time
import numpy as np
import random
import matplotlib.pyplot as plt 

npe = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H'] #Textbook example problem
width = [2, 1, 3, 3, 3, 5, 1, 2]
height = [4, 3, 3, 5, 2, 3, 2, 4]

# npe = [4,3,5,'H',1,'V',6,7,'V','H',2,'V',8,'H','V']
# width = [5, 2, 6, 2, 6, 5, 3, 6]
# height = [3, 3, 3, 5, 2, 1, 8, 3]

# npe = [1,2,'H',3,4,'H',5,'H','V']
# width = [4, 4, 3, 4, 3]
# height = [6, 4, 4, 4, 4]

node = list(range(1,len(width)+1))
N = len(node)

# HV = [-1, -1, -1, -1, -2, -1]
# co=['green','yellow','pink','red','black','gray','blue']

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

            old_cost = area(s_temp)

            b = random.randint(1,3)

            if b == 1:
                M1(s_temp)
            elif b == 2:
                M2(s_temp)
            elif b == 3:
                M3(s_temp)

            totm += 1
            new_cost = area(s_temp)
            delta = new_cost - old_cost
            r = np.random.random()

            if (delta<0 or (r<np.exp(-delta/T))):
                
                if (delta > 0):
                    uphill += 1

                s = s_temp[:]

                if (area(s)<area(s_best)):
                    s_best = s[:]

            else:
                reject += 1
        
        T = 0.99 * T

        if (float(reject/totm) > 0.95):
            break
    
    time_taken = time.clock() - tic
    s = s_best[:]
    print("Final: ",s)
    print("Area  : ",area(s))
    print("Time: ",time_taken)


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

# def plotRectangles():
#     fig = plt.figure()
#     ax = fig.add_subplot(111) 

#     rect = matplotlib.patches.Rectangle((sumx, sumy), width[1], height[1],  color ='blue') 
#     ax.add_patch(rect) 
#     sumx=0
#     sumy=0
#     for i in range(N):
#         if HV[i]==-1:
#             sumy= sumy + height[i]
#             rect= matplotlib.patches.Rectangle((sumx,sumy), width[i+1], height[i+1], color =co[i]) 
#             ax.add_patch(rect) 
#         else:
#             sumx = sumx + width[i]
#             rect= matplotlib.patches.Rectangle((sumx,sumy), width[i+1], height[i+1], color =co[i])
#             ax.add_patch(rect)

#     plt.xlim([0, 30]) 
#     plt.ylim([0, 30]) 
  
#     plt.show() 

def newDimensions(w1,h1,w2,h2,hv):
    
    if hv=='H':
        width.append(max(w1,w2))
        height.append(h1 + h2)
    elif hv=='V':
        width.append(w1 + w2)
        height.append(max(h1,h2))

    # print("Width : ",width[len(width)-1])
    # print("Height: ",height[len(height)-1])


def area(s):
    s1 = s[:]
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
            newDimensions(width[int(s1[q-2])-1],height[int(s1[q-2])-1],width[int(s1[q-1])-1],height[int(s1[q-1])-1],s1[q])
            s1.pop(q) and s1.pop(q-1) and s1.pop(q-2)
            s1.insert(q-2,node[len(node)-1])
       
        # print(s1)

    final_width = width[len(width)-1]
    final_height = height[len(height)-1] 
    final_area = final_width * final_height
    # print("Width : ",final_width)
    # print("Height: ",final_height)
    # print("Area  : ",final_area)
    # print("")

    for i in range(2,N+1):
        width.pop(len(height)-1)
        height.pop(len(height)-1)
        node.pop(len(node)-1)

    return final_area


# module = {}
# for i in range(6):
#     node.append(i+1)
#     module[node[i]] = (width[i],height[i])
#     npe.append(node[i])
#     if i is not 0:
#         npe.append('V')


print("\nInitial : "), 
printNPE(npe)
final_area = area(npe)
print("Area  : ",final_area)
print("--------------------------------------------------------------------")

simulatedAnnealing(npe)
# M1(npe)
# M2(npe)
# M3(npe)
