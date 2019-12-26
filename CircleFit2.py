import numpy as np
posmat=np.genfromtxt('FiltPosition.csv')
or_rot_mat=np.genfromtxt('OrientationMatCam2Mark.csv')
iteratnp=np.linspace(3,or_rot_mat.shape[0]-3,(or_rot_mat.shape[0]-6)/3+1)
print('Iterator',iteratnp)
nxar=np.array([])
nyar=np.array([])
nzar=np.array([])
nxyzar=np.array([])
rmat1=np.transpose(or_rot_mat[0:3,:])
#print('Ref matrix',rmat1)
for i in iteratnp:
    rmat2=np.transpose(or_rot_mat[int(i):int(i)+3,0:3])
    #print('rmat2 shape',rmat2.shape) 
    rmat=np.matmul(np.linalg.inv(rmat1),rmat2)
    #print('rmat shape',rmat.shape) 
    drmat=0.5*(rmat-np.transpose(rmat))
    #print('drmat',drmat,drmat[2,0]*drmat[2,0]+drmat[1,0]*drmat[1,0]+drmat[2,1]*drmat[2,1])
    if (drmat[2,0]*drmat[2,0]+drmat[1,0]*drmat[1,0]+drmat[2,1]*drmat[2,1])<1:
        th=np.math.asin(np.math.sqrt(drmat[2,0]*drmat[2,0]+drmat[1,0]*drmat[1,0]+drmat[2,1]*drmat[2,1]))
        print('Theta rlative:',th*180/np.pi)

        if nxyzar.shape[0]==0: 
            nxyzar=np.array([np.math.sqrt(drmat[2,0]*drmat[2,0]+drmat[1,0]*drmat[1,0]+drmat[2,1]*drmat[2,1])])
            nyar=np.array([drmat[0,2]])
            nxar=np.array([drmat[2,1]])
            nzar=np.array([drmat[1,0]])

        else:
            nxyzar=np.vstack((nxyzar,np.array([np.math.sqrt(drmat[2,0]*drmat[2,0]+drmat[1,0]*drmat[1,0]+drmat[2,1]*drmat[2,1])])))
            nyar=np.vstack((nyar,np.array([drmat[0,2]])))
            nxar=np.vstack((nxar,np.array(drmat[2,1])))
            nzar=np.vstack((nzar,np.array([drmat[1,0]])))

    else:
        print('!!!!!!!!!!Sine Condition not met!!!!!!!!!!!')     

nxrot=np.array([np.sum(nxyzar*nxar)/np.math.pow(np.linalg.norm(nxyzar),2),np.sum(nxyzar*nyar)/np.math.pow(np.linalg.norm(nxyzar),2),np.sum(nxyzar*nzar)/np.math.pow(np.linalg.norm(nxyzar),2)])
nxrotnorm=nxrot/np.linalg.norm(nxrot)
nxrotnorm_cam2mark=np.matmul(rmat1,nxrotnorm)
print('nxyz from rotation matrices',nxrotnorm_cam2mark)                
normalcoeff=np.matmul(np.linalg.pinv(posmat[:,:3]),np.ones((posmat.shape[0],1)))
print('Mean residuals (position):',1000*np.mean(np.matmul(posmat[:,:3],normalcoeff)-np.ones((posmat.shape[0],1))))
print('Parameters:',normalcoeff)
print('Unit Normal:',normalcoeff/np.linalg.norm(normalcoeff))
print('Angle between Rotation and positions based:',180/np.pi*np.math.asin(np.linalg.norm(np.cross(np.transpose(normalcoeff/np.linalg.norm(normalcoeff)),nxrotnorm_cam2mark))))

u,d,v=np.linalg.svd(posmat[:,:3])
#print('U',u,'D',d,'V',v)
