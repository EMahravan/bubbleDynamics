L=-25
RBUBBLE=0.6

DELTAT=1e-07
ENDTIME=3

Nx=600 #total number of points in x direction
Ny=660 #total number of points in y direction

ac=138999.59

YFREESURFACE=0.

XBUBBLE=0
YBUBBLE=-6
Gamma1=1.25
Cp=2200
Cv=2200/1.25
R=Cp-Cv

UU=0.
VU=0.
pU=1.01325e5
rhoU=(pU/ac)**(1./Gamma1)

p01=0.

rhoD=1025.
UD=0.
VD=0.
pD=1.01325e5

ac=138999.59

pB=72.7e6
rhoB=(pB/ac)**(1./Gamma1)
UB=0.
VB=0.

Gamma2=4.4
p02=6e8

Cp2=4186
Cv2=Cp2/Gamma2

R2=Cp2-Cv2

M2=8314./R2

Cp1=2200
Cv1=Cp1/Gamma1

R1=Cp1-Cv1

M1=8314./R1


TU=pU/rhoU/R1
TD=TU
TB=pB/rhoB/R1

print "TU=",TU,"    pU=",pU,"    rhoU=",rhoU,"    Gamma1=",Gamma1,"    R1=",R1,"    Cp1=",Cp1
print "TD=",TD,"    pD=",pD,"    rhoD=",rhoD
print "TB=",TB,"    pB=",pB,"    rhoB=",rhoB

import numpy as np
import sys
import os

solver="GFMCompCompFoam"

case="2D"

os.system("rm -r "+case+"/0")
os.system("rm -r "+case+"/sets")


YMAX=  10.
YMIN= -100.
XMAX=  100.
XMIN=  0.
ZMIN=-0.0125*(XMAX-XMIN)
ZMAX= 0.0125*(XMAX-XMIN)

Lx=(XMAX-XMIN)
Ly=YMAX-YMIN
LyLxRatio=Ly/Lx #Ratio of domain hight to widgth


YMinUniform=-12
YMaxUniform=4

XMaxUniform=10

NxUniform=0.2*Nx
dUniform=XMaxUniform/NxUniform
NyUniform=int((YMaxUniform-YMinUniform)/dUniform)

#Define length ratios
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

#~ print "r=",r,"    XgrG1=",XgrG1,"   XgrN1=",XgrN1,"   L=",L,"    a=",a

while error>1e-8:
    #~ XgrG1=1-a/L*(1-r**(XgrN1+1))
    YgrG3=(1-(YgrL3*Ly)/a*(1-r))**(1./(YgrN3+1))
    
    error=abs(YgrG3-r)
    r=YgrG3
    
print "r=",r,"   YgrN3=",YgrN3,"   L=",L,"    a=",a
YgrG3=r**YgrN3

YgrN3=YgrN3*1.0/Ny


error=10
a=dUniform
YgrG1=1.001
r=YgrG1

#~ print "r=",r,"    XgrG1=",XgrG1,"   XgrN1=",XgrN1,"   L=",L,"    a=",a

while error>1e-8:
    #~ XgrG1=1-a/L*(1-r**(XgrN1+1))
    YgrG1=(1-(YgrL1*Ly)/a*(1-r))**(1./(YgrN1+1))
    
    error=abs(YgrG1-r)
    r=YgrG1
    
print "r=",r,"   YgrN1=",YgrN1,"   L=",L,"    a=",a

YgrG1=r**YgrN1
YgrG1=1./YgrG1
YgrG2=1

YgrN1=YgrN1*1.0/Ny
YgrN2=YgrN2*1.0/Ny

print "YgrG1=",YgrG1


##########################################################################################

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
print "r=",r,"   XgrN2=",XgrN2,"   L=",L,"    a=",a

XgrG2=r**XgrN2
XgrG1=1

XgrN1=XgrN1*1.0/Nx
XgrN2=XgrN2*1.0/Nx

blockMeshDictOrig=case+"/system/blockMeshDict.orig"
blockMeshDict=case+"/system/blockMeshDict"

os.system('sed -e s/LconvertToMeters/'+str(1.)+'/g  '+blockMeshDictOrig+' > '+blockMeshDict)

os.system('sed -i s/LyLxRatio/'+str(LyLxRatio)+'/g  '+blockMeshDict)

os.system('sed -i s/NX/'+str(Nx)+'/g  '+blockMeshDict)
os.system('sed -i s/NY/'+str(Ny)+'/g  '+blockMeshDict)
os.system('sed -i s/XMIN/'+str(XMIN)+'/g  '+blockMeshDict)
os.system('sed -i s/XMAX/'+str(XMAX)+'/g  '+blockMeshDict)
os.system('sed -i s/YMIN/'+str(YMIN)+'/g  '+blockMeshDict)
os.system('sed -i s/YMAX/'+str(YMAX)+'/g  '+blockMeshDict)
os.system('sed -i s/ZMIN/'+str(ZMIN)+'/g  '+blockMeshDict)
os.system('sed -i s/ZMAX/'+str(ZMAX)+'/g  '+blockMeshDict)


os.system('sed -i s/XgrN1/'+str(XgrN1)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrN2/'+str(XgrN2)+'/g  '+blockMeshDict)

os.system('sed -i s/XgrL1/'+str(XgrL1)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrL2/'+str(XgrL2)+'/g  '+blockMeshDict)

os.system('sed -i s/XgrG1/'+str(XgrG1)+'/g  '+blockMeshDict)
os.system('sed -i s/XgrG2/'+str(XgrG2)+'/g  '+blockMeshDict)

os.system('sed -i s/YgrN1/'+str(YgrN1)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrN2/'+str(YgrN2)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrN3/'+str(YgrN3)+'/g  '+blockMeshDict)

os.system('sed -i s/YgrL1/'+str(YgrL1)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrL2/'+str(YgrL2)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrL3/'+str(YgrL3)+'/g  '+blockMeshDict)

os.system('sed -i s/YgrG1/'+str(YgrG1)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrG2/'+str(YgrG2)+'/g  '+blockMeshDict)
os.system('sed -i s/YgrG3/'+str(YgrG3)+'/g  '+blockMeshDict)

transportPropertiesOrig=case+"/constant/transportProperties.orig"
transportProperties=case+"/constant/transportProperties"

setFieldsOrig=case+"/system/setFieldsDict.orig"
setFields=case+"/system/setFieldsDict"

os.system('sed -e s/YFREESURFACE/'+str(YFREESURFACE)+'/g  '+setFieldsOrig+' > '+setFields)
os.system('sed -i s/XBUBBLE/'+str(XBUBBLE)+'/g  '+setFields)
os.system('sed -i s/YBUBBLE/'+str(YBUBBLE)+'/g  '+setFields)
os.system('sed -i s/RBUBBLE/'+str(RBUBBLE)+'/g  '+setFields)
os.system('sed -i s/XMIN/'+str(XMIN)+'/g  '+setFields)
os.system('sed -i s/XMAX/'+str(XMAX)+'/g  '+setFields)
os.system('sed -i s/YMIN/'+str(YMIN)+'/g  '+setFields)
os.system('sed -i s/YMAX/'+str(YMAX)+'/g  '+setFields)
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

controlDictOrig=case+"/system/controlDict.orig"
controlDict=case+"/system/controlDict"
os.system('sed -e s/DELTAT/'+str(DELTAT)+'/g  '+controlDictOrig+' > '+controlDict)
os.system('sed -i s/ENDTIME/'+str(ENDTIME)+'/g  '+controlDict)
os.system('sed -i s/WRITEINTERVAL/'+str(400e-5)+'/g  '+controlDict)

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

os.system('sed -i s/LINF/'+str(L*coeff)+'/g  '+U0)
os.system('sed -i s/LINF/'+str(L*coeff)+'/g  '+p0)
os.system('sed -i s/LINF/'+str(L*coeff)+'/g  '+T10)
os.system('sed -i s/LINF/'+str(L*coeff)+'/g  '+p10)
os.system('sed -i s/LINF/'+str(L*coeff)+'/g  '+U10)

os.system('echo running blockMesh...')
os.system('blockMesh -case '+ case+' > '+case+'/log.blockMesh')
os.system('echo running setFields...')
os.system('setFields -case '+ case+' > '+case+'/log.setFields')
#~ os.system('echo running '+solver+' ...')
#~ os.system(solver+' -case '+ case+' > '+case+'/log.'+solver)
#~ os.system('echo running sample...')
#~ os.system('sample -case '+ case+' > '+case+'/log.sample')

print "R1=",R1,"   R2=",R2
