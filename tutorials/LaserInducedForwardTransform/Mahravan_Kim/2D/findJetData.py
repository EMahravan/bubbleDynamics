sampleDir="postProcessing/surfaces/" #Sample directory in your OpenFOAM Distro
variableName="U"
isVariableAVector=True
fileName=variableName+"_interface.vtk"  #Name of the output file

import os
import numpy as  np
import matplotlib.pyplot as plt

#A function which reads a file in a time directory inside sampleDir 
def extractJetData (timeName,JPos,JU):
   
    readDestination = sampleDir + timeName + "/raw_"+variableName+".dat"
    data=np.loadtxt(readDestination)
    data = data[np.argsort(data[:, 1])]
    
    JPos.append(data[-1,1])
    JU.append(data[-1,4])
    JD.append(data[-1,0])
    # ~ print data.shape[0]  , JPos , JU

#####  End of function 


#iterate on time directories and call the function for each directory
JPos=[]
JU=[]
JD=[]
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

# ~ print listDirStr

for dirStr in listDirStr:
    extractJetData( dirStr ,JPos,JU)
    print dirStr
    
# ~ #Inputs for plot


os.system('rm jetInfo.dat')

        
writeRaw = open("jetInfo.dat", "w")

for i in range(0,len(JPos),1):
    writeRaw.write(str(listDirFloat[i])+"  "+str(JPos[i])+"  "+str(JU[i])+"  "+str(JD[i])+"\n")
writeRaw.close()
        
