sampleDir="postProcessing/surfaces/" #Sample directory in your OpenFOAM Distro
variableName="U"
isVariableAVector=True
fileName=variableName+"_interface.vtk"  #Name of the output file

import os
import numpy as  np
import matplotlib.pyplot as plt
import time
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


#A function which reads a file in a time directory inside sampleDir 
def seperate( timeName ):
  if (float(timeName)<2.5e-6):
    # ~ print "rank: ",rank, "timeName: ",timeName
    readDestination = sampleDir + timeName + "/raw_"+variableName+".dat"
    data=np.loadtxt(readDestination)
    
    pointXSorted = data[np.argsort(data[:, 0])]#Sort data by x poisition

    freeSurface=[]
    freeSurface.append(pointXSorted.shape[0]-1)#Add the point with largest x as the first member. This point is definitely for free surface
    usedPointsMarker=np.full(pointXSorted.shape[0],-1)
    i=pointXSorted.shape[0]-1
    usedPointsMarker[i]=1#This marker prevents reuse of the points 
    
    minX=min(pointXSorted[:,0])
    prevDist=0
    # ~ while (pointXSorted[i,0]>1.1*minX):
    while (True):
        
        minDist=1e10
        minJ=-1
        # ~ print min(i+200,pointXSorted.shape[0]-1),max(-1,i-200), i
        for j in range(min(i+550,pointXSorted.shape[0]-1),max(-1,i-550),-1):#For 250 points before and after each point, search for the nearest

            if (usedPointsMarker[j]!=1):
                dist=((pointXSorted[i,0]-pointXSorted[j,0])**2+(pointXSorted[i,1]-pointXSorted[j,1])**2)**0.5
                
                if(dist<minDist):
                    minDist=dist
                    minJ=j
                    
        if(pointXSorted[i,0]<1e-6):
           
            if(minDist>5e-7 or i==0):#freeSurface[-1] should be equal to i, so we need one before it
                break
            
        freeSurface.append(minJ)
        usedPointsMarker[minJ]=1
            
        i=minJ    
    
        prevDist=minDist
        
        if(minJ==-1):
            print ("freesurface: minJ=-1")
            exit()
            
    writeDestination = sampleDir + timeName + "/freeSurface_"+variableName+".dat"
    os.system("rm "+writeDestination)
    writeRaw = open(writeDestination, "w")
    for i in freeSurface:
        writeRaw.write(str(pointXSorted[i,0])+"  "+str(pointXSorted[i,1])+"  "+str(pointXSorted[i,2])+"   "+str(pointXSorted[i,3])+"  "+str(pointXSorted[i,4])+"  "+str(pointXSorted[i,5])+"\n")

##############################################################
    pointYSorted = data[np.argsort(data[:, 1])]#Now sort points by y position. The first point is the lowest point which is for sure a point on bubble surface. Other points will be tracked as chain pieces
    freeSurface=[]

    usedPointsMarker.fill(-1)
    # ~ print usedPointsMarker
    i=0
    if(pointYSorted[i,0]<4e-6):
        for j in range(0,pointYSorted.shape[0]):
            i=j
            if pointYSorted[i,0]>3e-6:#This condition is not enough for some of higher times, when there are multiple contacts to the ground and two or one of them are connected to the main bubble
                break
    freeSurface.append(i)

    usedPointsMarker[i]=1
    
    while (True):
        # ~ print i, pointYSorted.shape[0]-1
        minDist=1e10
        minJ=-1
        for j in range(max(0,i-750),min(i+750,pointYSorted.shape[0])):
            # ~ print "TTTTTTTT"
            if (usedPointsMarker[j]!=1):
                dist=((pointYSorted[i,0]-pointYSorted[j,0])**2+(pointYSorted[i,1]-pointYSorted[j,1])**2)**0.5
                
                if(dist<minDist):
                    minDist=dist
                    minJ=j
                    # ~ print "dist:",dist,"minDist:",minDist, dist<minDist
                    
            # ~ print "Here"
            
        if (minDist>10e-7 or i==pointYSorted.shape[0]-1 or minJ==-1):#freeSurface[-1] should be equal to i, so we need one before it

            # ~ print "minDist=",minDist

            # ~ print "pointYSorted[i,1]=",pointYSorted[i,1], "   pointYSorted[i,0]=",pointYSorted[i,0]
            # ~ print "pointYSorted[j,1]=",pointYSorted[j,1], "   pointYSorted[j,0]=",pointYSorted[j,0]

            break
                
        freeSurface.append(minJ)
        usedPointsMarker[minJ]=1
        
       
        # ~ print "minDist=",minDist
        # ~ print "pointXSorted[i,0]=",pointXSorted[i,0],"pointXSorted[i,1]=",pointXSorted[i,1],"timeName: ",timeName
            
        i=minJ    
            
        
        if(minJ==-1):
            print ("bubble:  minJ=-1")
            break
            # ~ exit()
            
        
    writeDestination = sampleDir + timeName + "/bubble_"+variableName+".dat"
    os.system("rm "+writeDestination)
    writeRaw = open(writeDestination, "w")
    for i in freeSurface:
        writeRaw.write(str(pointYSorted[i,0])+"  "+str(pointYSorted[i,1])+"  "+str(pointYSorted[i,2])+"   "+str(pointYSorted[i,3])+"  "+str(pointYSorted[i,4])+"  "+str(pointYSorted[i,5])+"\n")


    writeRaw.close()
    
#####  End of function 
# ~ seperate( "1e-06" )

#iterate on time directories and call the function for each directory
dirList=os.listdir(sampleDir)
nDir=len(dirList)
dirPerProcess=nDir/size
first=int(dirPerProcess*rank)
last=int(dirPerProcess*(rank+1))
if (rank==(size-1)):
    last=nDir

# ~ seperate( "1.14e-06" )
for i in range(first, last, 1):
    print (dirList[i])
    seperate( dirList[i] )
    
