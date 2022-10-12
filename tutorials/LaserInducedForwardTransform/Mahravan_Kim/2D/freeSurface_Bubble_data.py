sampleDir="postProcessing/surfaces/" #Sample directory in your OpenFOAM Distro
variableName="U"
isVariableAVector=True
fileName=variableName+"_interface.vtk"  #Name of the output file

import os
import numpy as  np
import matplotlib.pyplot as plt

#A function which reads a file in a time directory inside sampleDir 
def extractJetData (timeName,JPos,JUX,JUY,BPos,BEqR,BUX,BUY):

    freeSurfaceDestination = sampleDir + timeName + "/freeSurface_"+variableName+".dat"
    bubbleDestination = sampleDir + timeName + "/bubble_"+variableName+".dat"
    freeSurfaceData=np.loadtxt(freeSurfaceDestination)
    bubbleData=np.loadtxt(bubbleDestination)
    
    bubbleVol=0
    for i in range (1,bubbleData.shape[0]):
        bubbleVol+=bubbleData[i,0]**2*(bubbleData[i,1]-bubbleData[i-1,1])
        
    bubbleVol=abs(bubbleVol*np.pi*2.)
    bubbleEqR=(bubbleVol/(4./3.*np.pi))**(1./3)
    BEqR.append(bubbleEqR)
    
    JPos.append(freeSurfaceData[-1,1])
    os.system("ls "+sampleDir + timeName)
    # ~ print "bubble shape: ", bubbleData.shape
    # ~ print "bubble pos: ", bubbleData[-1,1]
    BPos.append(bubbleData[-1,1])
    JUX.append(freeSurfaceData[-1,3])
    JUY.append(freeSurfaceData[-1,4])
    BUX.append(bubbleData[-1,3])
    BUY.append((bubbleData[-1,4]+bubbleData[-2,4]+bubbleData[-3,4]+bubbleData[-4,4])/4.)

#####  End of function 


#iterate on time directories and call the function for each directory
JPos=[]
JUX=[]
JUY=[]
BPos=[]
BEqR=[]
BUX=[]
BUY=[]
listDirFloat=[]
listDirStr=[]

for dirStr in os.listdir(sampleDir):
        listDirFloat.append(float(dirStr))
listDirFloat.sort()

for dirFloat in listDirFloat:
    for dirStr in os.listdir(sampleDir):
        if abs(float(dirStr)-dirFloat)<1e-15:
            listDirStr.append(dirStr)
            break

for dirStr in listDirStr:
  if (float(dirStr)<2.5e-6): 
    print (dirStr)
    extractJetData( dirStr ,JPos,JUX,JUY ,BPos,BEqR,BUX,BUY)
    
# ~ #Inputs for plot

os.system('rm freeSurface_Bubble_Info.dat')

        
writeRaw = open("freeSurface_Bubble_Info.dat", "w")

for i in range(0,len(JPos),1):
    writeRaw.write(str(listDirFloat[i])+"  "+str(JPos[i])+"  "+str(JUX[i])+"  "+str(JUY[i])+"  "+str(BPos[i])+"  "+str(BEqR[i])+"  "+str(BUX[i])+"  "+str(BUY[i])+"\n")
writeRaw.close()
        
