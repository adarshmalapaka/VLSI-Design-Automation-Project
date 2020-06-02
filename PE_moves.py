import math
import time
import numpy as np
import random

npe = []
node = []
width=[1, 1, 4, 2, 2, 1, 1]
height=[3, 3, 1, 2, 2, 1, 1]
HV=[-1, -1, -1, -1, -2, -1]

def printNPE(s):

    for i in range(len(s)):
        print(s[i]),  #end =" ")
  
    print("")


def M1(s):
    # swap two operands ignoring any operator chain
    A = []      
    for i in range(len(s)):
        if(s[i]!='V' and s[i]!='H'):  
            A.append(i); 
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

    while (True):
        r = random.randint(0,len(A)-1)
        k = A[r]   
        s[k+1], s[k] = s[k], s[k+1]
        if ((checkBallot(s) and checkSkewed(s)) is False):
            s[k], s[k+1] = s[k+1], s[k]
        else:
            break

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
    
# module = {}
# for i in range(6):
#     node.append(i+1)
#     module[node[i]] = (width[i],height[i])
#     npe.append(node[i])
#     if i is not 0:
#         npe.append('V')

# npe = [1,'H','V','H', 2, 'H', 'V', 3]
npe = ["2","1","3","5","4","6","H","7","V","H","V","10","8","V","9","H","12","V","H","16","H","18","11","13","H","20","V","H","15","14","H","V","21","H","V","19","H","V","H"]


print("Initial : "), 
printNPE(npe)

M1(npe)
print("After M1: "),
printNPE(npe)

M2(npe)
print("After M2: "),
printNPE(npe)

M3(npe)
print("After M3: "),
printNPE(npe)


