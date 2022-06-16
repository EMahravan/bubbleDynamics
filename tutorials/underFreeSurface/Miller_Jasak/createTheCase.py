#Author: Ehsan Mahravan
#Run this file to setup the case
#Parameters are selected based on: https://doi.org/10.1016/j.compfluid.2013.04.002

import numpy as np
import sys
import os

solver="compressibleInterFoam"
NPROCESSORS=4
case="2D"

#####Geometry

YMAX=  20.
YMIN= -100.
XMAX=  100.
XMIN=  0.
ZMIN=-0.0125*(XMAX-XMIN)
ZMAX= 0.0125*(XMAX-XMIN)

Lx=(XMAX-XMIN)
Ly=YMAX-YMIN
LyLxRatio=Ly/Lx #Ratio of domain height to width


RBUBBLE=0.6

YFREESURFACE=0.

#####DeltaT and number of grid cells

DELTAT=1e-07#Initial deltaT
WRITEINTERVAL=4e-03
ENDTIME=3

#This grid is quite coarse. Refine it to get a more accurate result.
Nx=280 #total number of cells in x direction
Ny=400 #total number of cells in y direction

#####Fluid properties
#1: gas
XBUBBLE=0
YBUBBLE=-6
Gamma1=1.25
Cp1=2200

ac1=138999.59#a_c=$p/\rho^\gamma$ (Eq. 9 in the paper)

Cv1=Cp1/Gamma1

R1=Cp1-Cv1

M1=8314./R1

#2: liquid
Gamma2=4.4
p02=6e8
Cp2=4186
Cv2=Cp2/Gamma2

R2=Cp2-Cv2

M2=8314./R2
#####Primary variables (Pressure, velocity and temperature)
#A: Initial values above the free-surface (atmosphere)
pA=1.01325e5 #U: (Up): Atmospheric pressure above the free-surface
rhoA=(pA/ac1)**(1./Gamma1)
TA=pA/rhoA/R1
UA=0

p01=0.

#D: (Down), initial values below the free-surface
rhoD=1025.
UD=0.
pD=1.01325e5

#B: Initial values for bubble
pB=72.7e6
rhoB=(pB/ac1)**(1./Gamma1)
UB=0.

TD=TA
TB=pB/rhoB/R1

print ("TA=",TA,"    pA=",pA,"    rhoA=",rhoA)
print ("TD=",TD,"    pD=",pD,"    rhoD=",rhoD)
print ("TB=",TB,"    pB=",pB,"    rhoB=",rhoB)

#####Grid cell distribution
#Uniform grid is preferred for an area around the bubble 
YMinUniform=-12
YMaxUniform=8

XMaxUniform=8

NxUniform=0.4*Nx
dUniform=XMaxUniform/NxUniform
NyUniform=int((YMaxUniform-YMinUniform)/dUniform)


#Knowing the size of the cell on the uniform grid and number of 
#the segments on the non-uniform side we can numerically calculate 
#the smallest to largest cell ratio for blockMeshDict 
##First for y direction
YgrL2=(YMaxUniform-YMinUniform)/Ly
YgrL1=(YMinUniform-YMIN)/Ly
YgrL3=(1-YgrL2-YgrL1)

YgrN1=int( (Ny-NyUniform)*YgrL1/(YgrL1+YgrL3) )
YgrN2=NyUniform
YgrN3=Ny-YgrN1-YgrN2

error=10
a=dUniform
YgrG3=1.001
r=YgrG3

while error>1e-8:
    #~ XgrG1=1-a/L*(1-r**(XgrN1+1))
    YgrG3=(1-(YgrL3*Ly)/a*(1-r))**(1./(YgrN3+1))
    
    error=abs(YgrG3-r)
    r=YgrG3
    
print ("r=",r,"   YgrN3=",YgrN3,"    a=",a)
YgrG3=r**YgrN3

YgrN3=YgrN3*1.0/Ny


error=10
a=dUniform
YgrG1=1.001
r=YgrG1

while error>1e-8:
    YgrG1=(1-(YgrL1*Ly)/a*(1-r))**(1./(YgrN1+1))
    
    error=abs(YgrG1-r)
    r=YgrG1
    
print ("r=",r,"   YgrN1=",YgrN1,"    a=",a)

YgrG1=r**YgrN1
YgrG1=1./YgrG1
YgrG2=1

YgrN1=YgrN1*1.0/Ny
YgrN2=YgrN2*1.0/Ny


##########################################################################################
##Now for x direction
XgrL1=XMaxUniform/Lx
XgrL2=(1-XgrL1)

XgrN1=NxUniform
XgrN2=(Nx-NxUniform)

error=10
a=dUniform
XgrG2=1.001
r=XgrG2

while error>1e-8:
    
    XgrG2=(1-(XgrL2*Lx)/a*(1-r))**(1./(XgrN2+1))
    
    error=abs(XgrG2-r)
    r=XgrG2
print ("r=",r,"   XgrN2=",XgrN2,"    a=",a)

XgrG2=r**XgrN2
XgrG1=1

XgrN1=XgrN1*1.0/Nx
XgrN2=XgrN2*1.0/Nx

#Having all the inputs, now we should setup the files
#Remove old files
os.system('rm -r '+ case+'/0 '+case+'/processor* '+case+'/log.* ')

#Create 0 directory
os.system('cp -r '+ case+'/0.orig '+ case+'/0')

#controlDict
controlDictOrig=case+"/system/controlDict.orig"
controlDict=case+"/system/controlDict"

os.system('sed -e s/DELTAT/'       +str(DELTAT)       +'/g  '+controlDictOrig+' > '+controlDict)
os.system('sed -i s/ENDTIME/'      +str(ENDTIME)      +'/g  '+controlDict)
os.system('sed -i s/WRITEINTERVAL/'+str(WRITEINTERVAL)+'/g  '+controlDict)

#blockMeshDict
blockMeshDictOrig=case+"/system/blockMeshDict.orig"
blockMeshDict=case+"/system/blockMeshDict"

os.system('sed -e s/LconvertToMeters/'+str(1.)+'/g  '+blockMeshDictOrig+' > '+blockMeshDict)
os.system('sed -i s/LyLxRatio/'+str(LyLxRatio)+'/g  '+blockMeshDict)
os.system('sed -i s/NX/'       +str(Nx)       +'/g  '+blockMeshDict)
os.system('sed -i s/NY/'       +str(Ny)       +'/g  '+blockMeshDict)
os.system('sed -i s/XMIN/'     +str(XMIN)     +'/g  '+blockMeshDict)
os.system('sed -i s/XMAX/'     +str(XMAX)     +'/g  '+blockMeshDict)
os.system('sed -i s/YMIN/'     +str(YMIN)     +'/g  '+blockMeshDict)
os.system('sed -i s/YMAX/'     +str(YMAX)     +'/g  '+blockMeshDict)
os.system('sed -i s/ZMIN/'     +str(ZMIN)     +'/g  '+blockMeshDict)
os.system('sed -i s/ZMAX/'     +str(ZMAX)     +'/g  '+blockMeshDict)
os.system('sed -i s/XgrN1/'    +str(XgrN1)    +'/g  '+blockMeshDict)
os.system('sed -i s/XgrN2/'    +str(XgrN2)    +'/g  '+blockMeshDict)
os.system('sed -i s/XgrL1/'    +str(XgrL1)    +'/g  '+blockMeshDict)
os.system('sed -i s/XgrL2/'    +str(XgrL2)    +'/g  '+blockMeshDict)
os.system('sed -i s/XgrG1/'    +str(XgrG1)    +'/g  '+blockMeshDict)
os.system('sed -i s/XgrG2/'    +str(XgrG2)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrN1/'    +str(YgrN1)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrN2/'    +str(YgrN2)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrN3/'    +str(YgrN3)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrL1/'    +str(YgrL1)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrL2/'    +str(YgrL2)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrL3/'    +str(YgrL3)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrG1/'    +str(YgrG1)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrG2/'    +str(YgrG2)    +'/g  '+blockMeshDict)
os.system('sed -i s/YgrG3/'    +str(YgrG3)    +'/g  '+blockMeshDict)

#transportProperties
transportPropertiesOrig=case+"/constant/transportProperties.orig"
transportProperties=case+"/constant/transportProperties"


#setFields
setFieldsOrig=case+"/system/setFieldsDict.orig"
setFields=case+"/system/setFieldsDict"

os.system('sed -e s/YFREESURFACE/'+str(YFREESURFACE)+'/g  '+setFieldsOrig+' > '+setFields)
os.system('sed -i s/XBUBBLE/'     +str(XBUBBLE)     +'/g  '+setFields)
os.system('sed -i s/YBUBBLE/'     +str(YBUBBLE)     +'/g  '+setFields)
os.system('sed -i s/RBUBBLE/'     +str(RBUBBLE)     +'/g  '+setFields)
os.system('sed -i s/XMIN/'        +str(XMIN)        +'/g  '+setFields)
os.system('sed -i s/XMAX/'        +str(XMAX)        +'/g  '+setFields)
os.system('sed -i s/YMIN/'        +str(YMIN)        +'/g  '+setFields)
os.system('sed -i s/YMAX/'        +str(YMAX)        +'/g  '+setFields)
os.system('sed -i s/ZMIN/'        +str(ZMIN)        +'/g  '+setFields)
os.system('sed -i s/ZMAX/'        +str(ZMAX)        +'/g  '+setFields)
os.system('sed -i s/pD/'          +str(pD)          +'/g  '+setFields)
os.system('sed -i s/TD/'          +str(TD)          +'/g  '+setFields)
os.system('sed -i s/UD/'          +str(UD)          +'/g  '+setFields)
os.system('sed -i s/pB/'          +str(pB)          +'/g  '+setFields)
os.system('sed -i s/TB/'          +str(TB)          +'/g  '+setFields)
os.system('sed -i s/UB/'          +str(UB)          +'/g  '+setFields)




p10=case+"/0/p_rgh"
os.system('sed -i s/PL1/'+str(pA)+'/g  '+p10)
os.system('sed -i s/PR1/'+str(pA)+'/g  '+p10)

p0=case+"/0/p"
os.system('sed -i s/PL2/'+str(pD)+'/g  '+p0)
os.system('sed -i s/PR2/'+str(pD)+'/g  '+p0)

T10=case+"/0/T"

os.system('sed -i s/TL1/'+str(TA)+'/g  '+T10)
os.system('sed -i s/TR1/'+str(TA)+'/g  '+T10)

U10=case+"/0/U"

os.system('sed -i s/UL1/'+str(UA)+'/g  '+U10)
os.system('sed -i s/UR1/'+str(UA)+'/g  '+U10)

U0=case+"/0/U"

os.system('sed -i s/UL2/'+str(UD)+'/g  '+U0)
os.system('sed -i s/UR2/'+str(UD)+'/g  '+U0)

L=50

os.system('sed -i s/LINF/'+str(L)+'/g  '+U0)
os.system('sed -i s/LINF/'+str(L)+'/g  '+p0)
os.system('sed -i s/LINF/'+str(L)+'/g  '+T10)
os.system('sed -i s/LINF/'+str(L)+'/g  '+p10)
os.system('sed -i s/LINF/'+str(L)+'/g  '+U10)

decomposeParDictOrig=case+"/system/decomposeParDict.orig"
decomposeParDict=case+"/system/decomposeParDict"

os.system('sed -e s/NPROCESSORS/'+str(NPROCESSORS)+'/g  '+decomposeParDictOrig+' > '+decomposeParDict)

print('running blockMesh...')
os.system('blockMesh -case '+ case+' > '+case+'/log.blockMesh')
print('running setFields...')
os.system('setFields -case '+ case+' > '+case+'/log.setFields')
print('running decomposePar...')
os.system('decomposePar -force -case '+ case+' > '+case+'/log.decomposePar')

print("Everything is sorted. You can run the case by: mpirun -np "
      +str(NPROCESSORS)+" "+solver+" -parallel -case "+case+" > "+case+"/log."+solver)
