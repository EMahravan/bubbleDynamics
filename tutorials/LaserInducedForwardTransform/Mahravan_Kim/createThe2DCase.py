#Author: Ehsan Mahravan
#Run this file to setup the case
#Parameters are selected based on: https://doi.org/10.1063/5.0060422

import numpy as np
import sys
import os

solver="isCompressibleInterFoam"
NPROCESSORS=4
case="2D"

#####Geometry
YMAX=  600e-6
YMIN=  0.
XMAX=  200e-6
XMIN=  0.
ZMIN=-0.0125*(XMAX-XMIN)
ZMAX= 0.0125*(XMAX-XMIN)
Lx=(XMAX-XMIN)
Ly=YMAX-YMIN
LyLxRatio=Ly/Lx #Ratio of domain hight to widgth


RBUBBLE=4.e-6

NProcessor=16

DELTAT=0.5e-08
ENDTIME=15e-6
WRITEINTERVAL=0.5e-7

RMax=60e-6
gama=0.

YOil=0.*RMax/10.

XBUBBLE=0
ZBUBBLE=0
YFREESURFACE=16e-6
YBUBBLE=gama*RMax + YOil
Gamma1=1.45
Cp1=1864
M1=29.466

R1=8314./M1
Cv1=Cp1/Gamma1

#R1=Cp1-Cv1
Cv1=R1-Cp1
UU=0.
VU=0.
pRef=117251.
TRef=382.59
rhoRef=pRef/(R1*TRef)
pU=101315
TU=293.15
rhoU=pU/(R1*TU)

p01=0.

rhoD=1123
UD=0.
VD=0.
pD=101315

pB=190e6
# ~ rhoB=(pB/ac)**(1./Gamma1)
rhoB=rhoRef*(pB/pRef)**(1./Gamma1)

UB=0.
VB=0.

Gamma2=7.15

Cv2=2200
Cp2=Cv2*Gamma2

R2=Cp2-Cv2

M2=8314./R2

TU=pU/rhoU/R1
TD=TU
TB=pB/rhoB/R1

print ("TU=",TU,"    pU=",pU,"    rhoU=",rhoU,"    Gamma1=",Gamma1,"    R1=",R1,"    Cp1=",Cp1,"    M1=",M1)
print ("TD=",TD,"    pD=",pD,"    rhoD=",rhoD)
print ("TB=",TB,"    pB=",pB,"    rhoB=",rhoB)

os.system("rm -r "+case+"/0")
os.system("rm -r "+case+"/sets")
os.system("rm -r "+case+"/constant/polyMesh")





XFine=120e-6
XUniform=80e-6
YUniform=250e-6

YMinUniform=0.
XMinUniform=0.
YMaxUniform=YBUBBLE+YUniform
XMaxUniform=XMinUniform+XUniform


MinUniform=0.
XMinUniform=0.
YMaxUniform=YBUBBLE+YUniform
XMaxUniform=XMinUniform+XUniform

#2e-07
dxUniform=16e-7
dyUniform=16e-7

print ('YMAX=',YMAX,'    YMaxUniform=',YMaxUniform)


NxUniform=int(XUniform/dxUniform)
NyUniform=int(YUniform/dyUniform)

dxUniform=XUniform/NxUniform
dyUniform=YUniform/NyUniform

NFine=NxUniform*1.5
Nx=int(NFine*1.3) #total number of points in x direction

NyRest=int((YMAX-YUniform)/dyUniform);

Ny=NyUniform+NyRest

print ('Ny=',Ny,'  NyUniform=', NyUniform,'  YMaxUniform=', YMaxUniform)
print ('Nx=',Nx,'  NxUniform=', NxUniform,'  NFine=', NFine,'  XMaxUniform=', XMaxUniform,'  XUniform=', XUniform,'  XFine=', XFine,'  YUniform=', YUniform)

##########################################################################################
#Define length ratios
YgrL2=(YMaxUniform-YMinUniform)/Ly
YgrL3=(1-YgrL2)

YgrN2=NyUniform
YgrN3=Ny-YgrN2

print ("YgrN2=",YgrN2,"    YgrN3=",YgrN3)
print ("YgrL3=",YgrL3,"    YgrL3=",YgrL3)

error=10
a=dyUniform
YgrG3=1.001
r=YgrG3

#~ print "r=",r,"    XgrG1=",XgrG1,"   XgrN1=",XgrN1,"   L=",L,"    a=",a

while error>1e-8:
    #~ XgrG1=1-a/L*(1-r**(XgrN1+1))
    YgrG3=(1-(YgrL3*Ly)/a*(1-r))**(1./(YgrN3+1))
    
    error=abs(YgrG3-r)
    r=YgrG3
    
print ("r=",r,"   YgrN3=",YgrN3,"    a=",a,"    aLast=",a*r**YgrN3)
YgrG3=r**YgrN3

YgrN3=YgrN3*1.0/Ny


YgrG2=1.
YgrN2=YgrN2*1.0/Ny
print ("r=",r,"   YgrN3=",YgrN3,"    YgrG3=",YgrG3,"   YgrN2=",YgrN2,"    YgrG2=",YgrG2)

##########################################################################################


XgrL1=XUniform/Lx
XgrL2=(XFine-XMaxUniform)/Lx
XgrL3=(1-XgrL1-XgrL2)

XgrN1=NxUniform
XgrN2=(NFine-NxUniform)
XgrN3=(Nx-NFine)

error=10
a=dxUniform
XgrG2=1.001
r=XgrG2

while error>1e-8:

    XgrG2=(1-(XgrL2*Lx)/a*(1-r))**(1./(XgrN2+1))
    
    error=abs(XgrG2-r)
    r=XgrG2
    
aLast2=a*r**XgrN2
print ("r=",r,"   XgrN2=",XgrN2,"    a=",a,"    aLast=",a*r**XgrN2)

XgrG2=r**XgrN2
XgrG1=1

XgrN1=XgrN1*1.0/Nx
XgrN2=XgrN2*1.0/Nx
###################
error=10
a=aLast2
XgrG3=1.001
r=XgrG3

while error>1e-8:
    
    XgrG3=(1-(XgrL3*Lx)/a*(1-r))**(1./(XgrN3+1))
    
    error=abs(XgrG3-r)
    r=XgrG3
print ("r=",r,"   XgrN3=",XgrN3,"    a=",a,"    aLast=",a*r**XgrN3)

XgrG3=r**XgrN3

XgrN3=XgrN3*1.0/Nx

##########################################################################################
blockMeshDictOrig=case+"/system/blockMeshDict.orig"
blockMeshDict=case+"/system/blockMeshDict"

os.system('sed -e s/LconvertToMeters/'+str(1.)+'/g  '+blockMeshDictOrig+' > '+blockMeshDict)

os.system('sed -i s/LyLxRatio/'+str(LyLxRatio)+'/g  '+blockMeshDict)

print ('NX=',Nx,'   Ny=',Ny)
os.system('sed -i s/NX/'+str(int(Nx))+'/g  '+blockMeshDict)
os.system('sed -i s/NY/'+str(int(Ny))+'/g  '+blockMeshDict)
os.system('sed -i s/XMIN/'+str(XMIN)+'/g  '+blockMeshDict)
os.system('sed -i s/XMAX/'+str(XMAX)+'/g  '+blockMeshDict)
os.system('sed -i s/YMIN/'+str(YMIN)+'/g  '+blockMeshDict)
os.system('sed -i s/YMAX/'+str(YMAX)+'/g  '+blockMeshDict)
os.system('sed -i s/ZMIN/'+str(ZMIN)+'/g  '+blockMeshDict)
os.system('sed -i s/ZMAX/'+str(ZMAX)+'/g  '+blockMeshDict)


os.system('sed -i s/XgrN1/'+str(XgrN1)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrN2/'+str(XgrN2)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrN3/'+str(XgrN3)+'/g  '+blockMeshDict)

os.system('sed -i s/XgrL1/'+str(XgrL1)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrL2/'+str(XgrL2)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrL3/'+str(XgrL3)+'/g  '+blockMeshDict)

os.system('sed -i s/XgrG1/'+str(XgrG1)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrG2/'+str(XgrG2)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrG3/'+str(XgrG3)+'/g  '+blockMeshDict)

os.system('sed -i s/YgrN2/'+str(YgrN2)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrN3/'+str(YgrN3)+'/g  '+blockMeshDict)

os.system('sed -i s/YgrL2/'+str(YgrL2)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrL3/'+str(YgrL3)+'/g  '+blockMeshDict)

os.system('sed -i s/YgrG2/'+str(YgrG2)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrG3/'+str(YgrG3)+'/g  '+blockMeshDict)

##########################################################################################
setFieldsOrig=case+"/system/setFieldsDict.orig"
setFields=case+"/system/setFieldsDict"

os.system('sed -e s/YOIL/'+str(YOil)+'/g  '+setFieldsOrig+' > '+setFields)
os.system('sed -i s/XBUBBLE/'+str(XBUBBLE)+'/g  '+setFields)
os.system('sed -i s/YBUBBLE/'+str(YBUBBLE)+'/g  '+setFields)
os.system('sed -i s/YFREESURFACE/'+str(YFREESURFACE)+'/g  '+setFields)
os.system('sed -i s/YMAX/'+str(YMAX)+'/g  '+setFields)
os.system('sed -i s/ZBUBBLE/'+str(ZBUBBLE)+'/g  '+setFields)
os.system('sed -i s/RBUBBLE/'+str(RBUBBLE)+'/g  '+setFields)
os.system('sed -i s/XMIN/'+str(XMIN)+'/g  '+setFields)
os.system('sed -i s/XMAX/'+str(XMAX)+'/g  '+setFields)
os.system('sed -i s/YMIN/'+str(YMIN)+'/g  '+setFields)
os.system('sed -i s/ZMIN/'+str(ZMIN)+'/g  '+setFields)
os.system('sed -i s/ZMAX/'+str(ZMAX)+'/g  '+setFields)

os.system('sed -i s/pD/'+str(pD)+'/g  '+setFields)
os.system('sed -i s/TD/'+str(TD)+'/g  '+setFields)
os.system('sed -i s/UD/'+str(UD)+'/g  '+setFields)
os.system('sed -i s/pU/'+str(pU)+'/g  '+setFields)
os.system('sed -i s/TU/'+str(TU)+'/g  '+setFields)
os.system('sed -i s/UU/'+str(UU)+'/g  '+setFields)
os.system('sed -i s/pB/'+str(pB)+'/g  '+setFields)
os.system('sed -i s/TB/'+str(TB)+'/g  '+setFields)
os.system('sed -i s/UB/'+str(UB)+'/g  '+setFields)



##########################################################################################
controlDictOrig=case+"/system/controlDict.orig"
controlDict=case+"/system/controlDict"
os.system('sed -e s/DELTAT/'+str(DELTAT)+'/g  '+controlDictOrig+' > '+controlDict)
os.system('sed -i s/ENDTIME/'+str(ENDTIME)+'/g  '+controlDict)
os.system('sed -i s/WRITEINTERVAL/'+str(WRITEINTERVAL)+'/g  '+controlDict)

os.system('rm -rf '+ case+'/0 '+case+'/log.* ')
os.system('rm -rf '+ case+'/0 '+case+'/sets ')

os.system('cp -r '+ case+'/0.orig '+ case+'/0')

os.system('rm -rf '+ case+'/0 '+case+'/log.* ')
os.system('rm -rf '+ case+'/0 '+case+'/sets ')

os.system('cp -r '+ case+'/0.orig '+ case+'/0')


p10=case+"/0/p_rgh"
os.system('sed -i s/PL1/'+str(pU)+'/g  '+p10)
os.system('sed -i s/PR1/'+str(pU)+'/g  '+p10)

p0=case+"/0/p"
os.system('sed -i s/PL2/'+str(pD)+'/g  '+p0)
os.system('sed -i s/PR2/'+str(pD)+'/g  '+p0)

T10=case+"/0/T"

os.system('sed -i s/TL1/'+str(TU)+'/g  '+T10)
os.system('sed -i s/TR1/'+str(TU)+'/g  '+T10)

U10=case+"/0/U"

os.system('sed -i s/UL1/'+str(UU)+'/g  '+U10)
os.system('sed -i s/UR1/'+str(UU)+'/g  '+U10)

U0=case+"/0/U"

os.system('sed -i s/UL2/'+str(UD)+'/g  '+U0)
os.system('sed -i s/UR2/'+str(UD)+'/g  '+U0)

coeff=2.

os.system('sed -i s/LINF/'+str(Lx*coeff)+'/g  '+U0)
os.system('sed -i s/LINF/'+str(Lx*coeff)+'/g  '+p0)
os.system('sed -i s/LINF/'+str(Lx*coeff)+'/g  '+T10)
os.system('sed -i s/LINF/'+str(Lx*coeff)+'/g  '+p10)
os.system('sed -i s/LINF/'+str(Lx*coeff)+'/g  '+U10)


decomposeParDictOrig=case+"/system/decomposeParDict.orig"
decomposeParDict=case+"/system/decomposeParDict"
os.system('sed -e s/NPROCESSOR/'+str(NProcessor)+'/g  '+decomposeParDictOrig+' > '+decomposeParDict)

os.system('echo running blockMesh...')
os.system('blockMesh -case '+ case+' > '+case+'/log.blockMesh')


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
topoSetDictL1Orig=case+"/system/topoSetDictL1.orig"
topoSetDictL1=case+"/system/topoSetDict"
os.system('cat '+topoSetDictL1)
XMinBubble=-1
YMinBubble=-1
XMaxBubble=RMax
YMaxBubble=1.8*RMax
XMinJet=0.
XMaxJet=14e-6
YMaxJet=YMAX*2
YMaxJet=YMAX*2
YMaxFreesurface=YFREESURFACE*1.5

os.system('sed -e s/XMinBubble/'+str(XMinBubble)+'/g  '+topoSetDictL1Orig+' > '+topoSetDictL1)
os.system('sed -i s/YMinBubble/'+str(YMinBubble)+'/g  '+topoSetDictL1)
os.system('sed -i s/XMaxBubble/'+str(XMaxBubble)+'/g  '+topoSetDictL1)
os.system('sed -i s/YMaxBubble/'+str(YMaxBubble)+'/g  '+topoSetDictL1)
os.system('sed -i s/YMaxFreesurface/'+str(YMaxFreesurface)+'/g  '+topoSetDictL1)
os.system('sed -i s/XMinJet/'+str(XMinJet)+'/g  '+topoSetDictL1)
os.system('sed -i s/XMaxJet/'+str(XMaxJet)+'/g  '+topoSetDictL1)
os.system('sed -i s/YMaxJet/'+str(YMaxJet)+'/g  '+topoSetDictL1)
os.system('sed -i s/ZMin/'+str(ZMIN)+'/g  '+topoSetDictL1)
os.system('sed -i s/ZMax/'+str(ZMAX)+'/g  '+topoSetDictL1)
##########################################################################################
os.system('topoSet -case '+ case+' > '+case+'/log.topoSet1')

refineMeshDictOrig=case+"/system/refineMeshDict.orig"
refineMeshDict=case+"/system/refineMeshDict"

os.system('sed -e s/SET/L1/g  '+refineMeshDictOrig+' > '+refineMeshDict)

os.system('refineMesh -dict system/refineMeshDict -overwrite > log.refineMesh')
os.system('rm constant/polyMesh/sets')
os.system('topoSet -case '+ case+' > '+case+'/log.topoSet1')
os.system('refineMesh -dict system/refineMeshDict -overwrite > log.refineMesh')
os.system('rm constant/polyMesh/sets')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
topoSetDictL2Orig=case+"/system/topoSetDictL2.orig"
topoSetDictL2=case+"/system/topoSetDict"

os.system('sed -e s/XMaxBubble/'+str(XMaxBubble)+'/g  '+topoSetDictL2Orig+' > '+topoSetDictL2)
os.system('sed -i s/YMaxBubble/'+str(YMaxBubble)+'/g  '+topoSetDictL2)
os.system('sed -i s/ZMin/'+str(ZMIN)+'/g  '+topoSetDictL2)
os.system('sed -i s/ZMax/'+str(ZMAX)+'/g  '+topoSetDictL2)


##########################################################################################
os.system('topoSet -case '+ case+' > '+case+'/log.topoSet2')

refineMeshDictOrig=case+"/system/refineMeshDict.orig"
refineMeshDict=case+"/system/refineMeshDict"
os.system('sed -e s/SET/L2/g  '+refineMeshDictOrig+' > '+refineMeshDict)

os.system('refineMesh -dict system/refineMeshDict -overwrite')

os.system('extrudeMesh -case '+ case+' > '+case+'/log.extrudeMesh')


os.system('echo running setFields...')
os.system('setFields -case '+ case+' > '+case+'/log.setFields')

