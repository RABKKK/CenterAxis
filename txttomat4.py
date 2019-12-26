import re
import numpy as np
import csv
from numpy import savetxt
import cv2 as cv
#matval=np.array('empty')
matval=np.array([])
positm=np.array([])
orientm=np.array([])
posit_cam2markm=np.array([])
orientmat_cam2markm=np.array([])
with open('RvecTvecFIle.txt') as f:
    cnt=0
    for line in f:
        cnt+=1
        print('Input:',line)
        data = line.split()
        print('Split:',re.split('\d+',data[0]))
        spltcont=re.split('[[]|[;]|[]]|[[]]|[\n]|[ ]',line)
        print('Split delimiter:',spltcont)
        if len(spltcont)==7:
            matval=np.vstack((matval,np.array([[float(spltcont[1])],[float(spltcont[4])]])))
        elif matval.shape[0]!=0:
            matval=np.vstack((matval,np.array([float(spltcont[1])])))
        else:
            matval=np.array([float(spltcont[1])])
        if matval.shape[0]%6==0 and matval[matval.shape[0]-1,0]>0:
            orient=np.array(([matval[matval.shape[0]-6,0],matval[matval.shape[0]-5,0],matval[matval.shape[0]-4,0]]))
            orientmat_cam2mark,jorientmat_cam2mark=cv.Rodrigues(orient)
            posit=np.array(([matval[matval.shape[0]-3,0],matval[matval.shape[0]-2,0],matval[matval.shape[0]-1,0]]))
            posit_cam2mark=-np.matmul(np.transpose(orientmat_cam2mark),posit)
            if positm.shape[0]==0:
                positm=posit
                posit_cam2markm=posit_cam2mark
                orientm=orient
                orientmat_cam2markm=np.transpose(orientmat_cam2mark)                            
            else:
                positm=np.vstack((positm,posit))
                posit_cam2markm=np.vstack((posit_cam2markm,posit_cam2mark))
                orientm=np.vstack((orientm,orient))
                orientmat_cam2markm=np.vstack((orientmat_cam2markm,np.transpose(orientmat_cam2mark)))            
        print('Find:',re.findall('\d+',data[0]))
        #a1.append(int(data[0]))
        #a2.append(int(data[1]))
        #a3.append(int(data[2]))
        #a4.append(int(data[3]))
    print('FInal matrix',matval,'Position:',positm,'Orientation:',orientm)
    print('Shapes:',matval.shape,positm.shape,orientm.shape)
savetxt('Position.csv',positm)
savetxt('Orientation.csv',orientm)
savetxt('PositionCam2Mark.csv',posit_cam2markm)
savetxt('OrientationMatCam2Mark.csv',orientmat_cam2markm)
#with open('Position.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    for l in positm:
#        writer.writerows([string(l[0]),l[1],l[2]])
#        #for val in l:       
#        #    writer.writerows([val])
#with open('Orientation.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    for l in orientm:
#        writer.writerows(l)
#        for val in l:       
#            writer.writerows(val)
