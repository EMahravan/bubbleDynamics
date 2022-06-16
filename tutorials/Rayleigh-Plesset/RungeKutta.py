import numpy as np

class RungeKutta:
   'Common base class for all employees'
   p=4
   q=0.1
   def __init__(self, start, end, N, NEqs,mu):
       self.start=start
       self.end=end
       self.N=N
       self.NEqs=NEqs
       self.mu=mu
       
       self.h=(self.end-self.start)/self.N
   
##########################################################
########################    RK4   ########################
   def RK4(self, t, w):
       K=np.zeros((self.NEqs, 4))
       RKt=np.array([t , t+self.h/2, t+self.h/2, t+self.h])
       RKCoeff=np.array([0.0,2.0,2.0,1.0])

       K[:,0]=self.h*f( RKt[0] , w[:],self.mu)
       

       for i in range(1,4):
            K[:,i]=self.h*f( RKt[i] , w[:]+K[:,i-1]/RKCoeff[i],self.mu )
       
       
       return w[:]+(K[:,0]+2*K[:,1]+2*K[:,2]+K[:,3])/6.0

##############################################################
########################    RK4 Loop  ########################
       
   def RK4Loop(self,w,a,b):
       RungeKutta.p=a
       RungeKutta.q=b
       for i in range(0,self.N):
            t=i*self.h
            w[:,i+1]=self.RK4(t, w[:,i])
            

def f(t,y,mu):
    rho=1123.
    R0=RungeKutta.p
    pv=2000
    p_inf=101323
    pg0=RungeKutta.q
    sigma=0.037
    n=1.45
    
    return np.array([y[1], ((pv-p_inf)+pg0*(R0/y[0])**(3.*n)-2*sigma/y[0]-4.*y[1]*mu/y[0] -1.5*rho*y[1]**2)/rho/y[0]  ])
