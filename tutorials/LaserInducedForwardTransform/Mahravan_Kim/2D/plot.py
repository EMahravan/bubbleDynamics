import os
import numpy as  np
import matplotlib.pyplot as plt



plt.rc('text', usetex=True)
plt.rc('font', family='serif')

zoom=0.7

fig, (ax1) = plt.subplots(1, 1)
w, h = fig.get_size_inches()
fig.set_size_inches(w * zoom, h * zoom)
fig.tight_layout() # Or equivalently,  "plt.tight_layout()"

data=np.loadtxt("jetInfo.dat")
Duocastella=np.loadtxt("Duocastella_2008.dat")
plt.scatter(Duocastella[:,0],Duocastella[:,1], label="Experiment", color='black')
plt.xlim(0, 9)
plt.plot(data[:,0]*1e6,data[:,1]*1e6,  label="Numeric", color='black')


plt.ylabel("$z_f(\mathrm{\mu m})$",fontsize=10)
plt.xlabel("$t(\mathrm{\mu s})$",fontsize=10)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.legend(loc="lower right",fontsize=10)
plt.tight_layout()

plt.savefig("plots/16_JetPos_Validation.eps")
plt.savefig("plots/16_JetPos_Validation.svg")

plt.figure()
plt.plot(data[:,0]*1e6,data[:,2], color='black')

plt.ylabel("$u_f$ (m/s)",fontsize=18); 
plt.xlabel("$t$ ($\mu s$)",fontsize=18); 
plt.xlim(0, 9)
plt.xticks(fontsize=16 )
plt.yticks(fontsize=16 )
plt.tight_layout()

plt.savefig("plots/JetU_mainCase.eps")
plt.savefig("plots/JetU_mainCase.svg")

plt.show()
