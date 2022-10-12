sampleDir="postProcessing/surfaces/" #Sample directory in your OpenFOAM Distro
variableName="U"
isVariableAVector=True
fileName=variableName+"_interface.vtk"  #Name of the output file

import os
import numpy as  np
import matplotlib.pyplot as plt


plt.rc('text', usetex=True)
plt.rc('font', family='serif')

timeNames=["1.1e-06","1.2e-06","1.25e-06"]
linestyles = ['-', '--', ':', '-.']
i=0
for timeName in timeNames:
    freeSurfaceDestination = sampleDir + timeName + "/freeSurface_"+variableName+".dat"
    bubbleDestination = sampleDir + timeName + "/bubble_"+variableName+".dat"
    freeSurfaceData=np.loadtxt(freeSurfaceDestination)
    bubbleData=np.loadtxt(bubbleDestination)
    
    plt.plot( bubbleData[:,0]*1e6,  -bubbleData[:,1]*1e6, label="t="+str(float(timeName)/1e-6)+"$\mu s$",color='black',linestyle=linestyles[i])
    plt.plot( -bubbleData[:,0]*1e6,  -bubbleData[:,1]*1e6, label="t="+str(float(timeName)/1e-6)+"$\mu s$",color='black',linestyle=linestyles[i])
    i=i+1

plt.ylabel("$z(\mu m)$",fontsize=18)
plt.xlabel("$x(\mu m)$",fontsize=18)
plt.xticks(fontsize=16 )
plt.yticks(fontsize=16 )
plt.axis('scaled')

plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
plt.xlim(-60, 60)
plt.ylim(-110, 0)
plt.legend(loc="lower right",fontsize=14)
# ~ plt.legend(bbox_to_anchor=(1.05, 1),fontsize=14)

plt.tight_layout()

# ~ plt.subplots_adjust(left=-0.1)


plt.savefig("plots/bubble_evolution_mainCase.eps") 

plt.show() 
