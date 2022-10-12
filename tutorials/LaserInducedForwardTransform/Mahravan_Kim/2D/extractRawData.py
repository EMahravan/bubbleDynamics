sampleDir="postProcessing/surfaces/" #Sample directory in your OpenFOAM Distro
variableName="U"
isVariableAVector=True
fileName=variableName+"_interface.vtk"  #Name of the output file

import os
import numpy as  np
import matplotlib.pyplot as plt
import vtk
from vtk.util import numpy_support as VN

#A function which reads a file in a time directory inside sampleDir 
def extractRawData( timeName ):

    readDestination = sampleDir + timeName + "/"+fileName
     
    writeDestination = sampleDir + timeName + "/raw_"+variableName+".dat"
    os.system("rm "+writeDestination)
    
    writeRaw = open(writeDestination, "w")
    
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(readDestination)
    reader.ReadAllVectorsOn()  # Activate the reading of all vectors
    reader.Update()
    data=reader.GetOutput()
    U = VN.vtk_to_numpy(data.GetPointData().GetArray('U'))

    i=0
    
    for u in U:
       point=data.GetPoint(i)
       if point[2]>0.:
           writeRaw.write(str(point[0])+"  "+str(point[1])+"  "+str(0.)+"   "+str(u[0])+"  "+str(u[1])+"  "+str(0.)+"\n")
       i=i+1
    writeRaw.close()
    
#####  End of function 


#iterate on time directories and call the function for each directory
for dirStr in os.listdir(sampleDir):
    extractRawData( dirStr )
    print dirStr
