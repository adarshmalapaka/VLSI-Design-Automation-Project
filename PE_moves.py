import math
import time
import numpy as np
import random

npe = []
node = []

node = [1, 2, 3, 4, 5, 6, 7, 8]

N = len(node)

npe = [2,5,'V',1,'H',3,7,4,'V','H',6,'V',8,'V','H']
width = [2, 1, 3, 3, 3, 5, 1, 2]
height = [4, 3, 3, 5, 2, 3, 2, 4]

# npe = [4,3,5,'H',1,'V',6,7,'V','H',2,'V',8,'H','V']
# width = [5, 2, 6, 2, 6, 5, 3, 6]
# height = [3, 3, 3, 5, 2, 1, 8, 3]

HV = [-1, -1, -1, -1, -2, -1]

def printNPE(s):

    for i in range(len(s)):
        print(s[i]),  #end =" ")
  
    print("")


def M1(s):
    # swap two operands ignoring any operator chain
    A = []      
    for i in range(len(s)):
        if(s[i]!='V' and s[i]!='H'):  
            A.append(i)
    r = random.randint(0,len(A)-2)
    s[A[r]], s[A[r+1]] = s[A[r+1]], s[A[r]] 
    
    print("After M1: "),
    printNPE(s)
    area(s)
    print("--------------------------------------------------------------------")

def M2(s):
    A = []   
    # j = 0   
    for i in range(len(s)-1):
        if ((s[i]!='V' and s[i]!='H') and (s[i+1]=='H' or s[i+1]=='V')):
            A.append(i+1)
            # j += 1
    r = random.randint(0,len(A)-1)
    # r = random.randint(0,j-1)
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
    
    print("After M2: "),
    printNPE(s)
    area(s)
    print("--------------------------------------------------------------------")

def M3(s):
    A = []
    for i in range(len(s)-1):
        if((s[i]!='V' and s[i]!='H') and (s[i+1]=='H' or s[i+1]=='V')):
            A.append(i)

    while (True):
        r = random.randint(0,len(A)-1)
        k = A[r]   
        s[k+1], s[k] = s[k], s[k+1]
        if ((checkBallot(s) and checkSkewed(s)) is False):
            s[k], s[k+1] = s[k+1], s[k]
        else:
            break

    print("After M3: "),
    printNPE(s)
    area(s)
    print("--------------------------------------------------------------------")

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

def newDimensions(w1,h1,w2,h2,hv):
    if hv=='H':
        width.append(max(w1,w2))
        height.append(h1 + h2)
    elif hv=='V':
        width.append(w1 + w2)
        height.append(max(h1,h2))


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
       
        print(s1)

    final_width = width[len(width)-1]
    final_height = height[len(height)-1] 
    final_area = final_width * final_height
    print("Width : ",final_width)
    print("Height: ",final_height)
    print("Area  : ",final_area)
    print("")

    for i in range(2,N+1):
        width.pop(len(height)-1)
        height.pop(len(height)-1)
        node.pop(len(node)-1)


# module = {}
# for i in range(6):
#     node.append(i+1)
#     module[node[i]] = (width[i],height[i])
#     npe.append(node[i])
#     if i is not 0:
#         npe.append('V')


print("\nInitial : "), 
printNPE(npe)
area(npe)
print("--------------------------------------------------------------------")

M1(npe)
M2(npe)
M3(npe)
