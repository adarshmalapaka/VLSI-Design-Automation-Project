
import matplotlib 
import matplotlib.pyplot as plt 
width=[1, 1, 4, 2, 2, 1, 1]
height=[3, 3, 1, 2, 2, 1, 1]
HV=[-1, -1, -1, -2, -2, -1]
co=['green','yellow','blue','red','black','blue']
print(width,height)
sumx=0
sumy=0  
  
fig = plt.figure() 
ax = fig.add_subplot(111) 
rect = matplotlib.patches.Rectangle((sumx, sumy), 
                                     width[1], height[1], 
                                     color ='blue') 
ax.add_patch(rect) 
for i in range(6):
	if HV[i]==-1:
		sumy= sumy + height[i]
		rect= matplotlib.patches.Rectangle((sumx,sumy), width[i+1], height[i+1], color =co[i]) 
		ax.add_patch(rect) 
	else:
		sumx=sumx + width[i]
		rect= matplotlib.patches.Rectangle((sumx,sumy), width[i+1], height[i+1], color =co[i])
		ax.add_patch(rect) 
plt.xlim([0, 6]) 
plt.ylim([0, 10]) 
  
plt.show() 
