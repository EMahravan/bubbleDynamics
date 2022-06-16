#This code solves Rayleigh-Plesset equation using Runge-Kutta method
#Two conditions for bubble are considered and plotted in the same graph

from os import system, remove
import numpy as np
import matplotlib.pyplot as plt
import RungeKutta as rk
plt.rc('text', usetex=True)#Write false if you don't have latex installed. with latex the graph is much fancier.
plt.rc('font', family='Serif')# If this does not work: sudo apt install msttcorefonts -qq   , then: rm 

#First and last time
start=0.0; end=0.00003
#Number of iterations. If it diverged increase this number 
N= 50000
#Number of the coupled equations
NEqs=2 

#Initial bubble radius
R0=4e-6         
#Liquid viscosity
mu_liquid=7.5e-3
#Bubble initial pressure
PB=190e6        

#Initial condition of the first and second equations
w=range(N+1)
w=np.zeros((NEqs, N+1))
w[0,0]=R0
w[1,0]=0

#Initialise the object
RK=rk.RungeKutta(start, end, N, NEqs,mu_liquid)
#Call the solver
RK.RK4Loop(w,R0,PB)

#Array t is required for plot
t = np.linspace(start, end, N+1)


plt.plot(t,w[0,:],linestyle="-",color="black",label="Bubble 1")

maxR_bubble1=max(w[0,:])




#Initial bubble radius
R0=1.26e-6
#Liquid viscosity
mu_liquid=7.5e-03
PB=5e9#Bubble initial pressure
#Initial condition of the first and second equations
w=range(N+1)
w=np.zeros((NEqs, N+1))
w[0,0]=R0
w[1,0]=0

#Initialise the object
RK=rk.RungeKutta(start, end, N, NEqs,mu_liquid)
#Call the solver
RK.RK4Loop(w,R0,PB)
#Add the second bubble to the plot
plt.plot(t,w[0,:],linestyle=":",color="black",label="Bubble 2")
maxR_bubble2=max(w[0,:])
plt.xlabel(r"$t(s)$")
plt.ylabel(r"$r(m)$")
plt.legend()
plt.savefig("Radius.eps")

print ("Maxim radius of the bubble 1: ",maxR_bubble1," Maxim radius of the bubble 2: ",maxR_bubble2)


plt.show()

