import os
import numpy as  np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

linestyles = ['-', '--', ':', '-.']


plt.rc('text', usetex=True)
plt.rc('font', family='serif')

data=np.loadtxt("freeSurface_Bubble_Info.dat")



smootheBeggin=int(2.5*data.shape[0]/4.)
smootheEnd=data.shape[0]-1
print data[smootheBeggin,0]
print data[smootheEnd,0]
print data.shape[0]
print smootheBeggin
smoothed = savgol_filter(data[smootheBeggin:smootheEnd,4], 101, 3)
data[smootheBeggin:smootheEnd,4]=smoothed
# ~ plt.xlim(0, 9)
plt.plot(data[:,0]*1e6,data[:,1]*1e6,  label="jet", color='black', linestyle=linestyles[0])
plt.plot(data[:,0]*1e6,data[:,4]*1e6,  label="bubble", color='black', linestyle=linestyles[1])
# ~ plt.plot(data[:,0]*1e6,yhat,  label="bubble", color='blue', linestyle=linestyles[1])


plt.ylabel("$z_f(\mu m)$",fontsize=18)
plt.xlabel("$t(\mu s)$",fontsize=18)
plt.xticks(fontsize=16 )
plt.yticks(fontsize=16 )
plt.xlim(0, 2)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), color='black')

plt.legend(loc="upper left",fontsize=14)
plt.tight_layout()

plt.savefig("plots/BubbleJetPos_mainCase.eps")

plt.figure()
smoothed = savgol_filter(data[smootheBeggin:smootheEnd,7], 101, 3)
data[smootheBeggin:smootheEnd,7]=smoothed

plt.plot(data[:,0]*1e6,data[:,3],    label="jet", color='black', linestyle=linestyles[0])
plt.plot(data[:,0]*1e6,data[:,7],  label="bubble", color='black', linestyle=linestyles[1])
# ~ plt.plot(data[:,0]*1e6,yhat,  label="bubble", color='blue', linestyle=linestyles[1])

plt.ylabel("$u_f$ (m/s)",fontsize=18)
plt.xlabel("$t$ ($\mu s$)",fontsize=18)
plt.xlim(0, 2)
plt.xticks(fontsize=16 )
plt.yticks(fontsize=16 )
plt.tight_layout()
plt.legend(loc="upper right",fontsize=14)

plt.savefig("plots/BubbleJetU_mainCase.eps")

plt.figure()
plt.plot(data[:,0]*1e6,data[:,5], color='black')

plt.ylabel("$R$ (m)",fontsize=18)
plt.xlabel("$t$ ($\mu s$)",fontsize=18)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), color='black')

plt.xlim(0, 2)
plt.xticks(fontsize=16 )
plt.yticks(fontsize=16 )
plt.tight_layout()
plt.legend(loc="upper right",fontsize=14)

plt.savefig("plots/BubbleR_mainCase.eps")

plt.show()



