import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import math
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
posmat=np.genfromtxt('Position.csv')
refposmat=np.array([])
for val in posmat:
    if val[2]>0:
        if refposmat.shape[0]==0:
            refposmat=np.array([val[0],val[1],val[2],0])
            inval=val
        else:            
            indist=np.power(np.sum((val-inval)*(val-inval)),0.5)
            if indist<np.power(2,0.5)*0.09:#maximum distance of diagonal
                refposmat=np.vstack((refposmat,np.array([val[0],val[1],val[2],0])))  
                refposmat[-1,3]=indist
np.savetxt('FiltPosition.csv',refposmat)
ax.scatter(refposmat[:,0],refposmat[:,1],refposmat[:,2],c=refposmat[:,3]/np.max(refposmat[:,3]))
#ax.plot(refposmat[:,0],refposmat[:,1],refposmat[:,2])
plt.xlim(-0.1,0.06)
plt.ylim(-0.06,.1)
#ax.zlim()

plt.show()


     
