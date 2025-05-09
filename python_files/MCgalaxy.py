#essential modules
import numpy as np
import matplotlib.pyplot as plt

#essential imports
from Body import Body

#function: initialize array of bodies in a galaxy
def generateGalaxy(r0,rb0, m0, mb0, N, L):
    #divide mass of galaxy among N masses
    m = m0/N
    #generate N bodies
    bodies = []
    for i in range(N):
        #position from normalized distribution p(R) = (1/r0)exp(-r/r0)
        r = -r0*np.log(1.0-np.random.rand())
        if r < L:
            theta = 2.0*np.pi*np.random.rand()
            rx = r*np.cos(theta)
            ry = r*np.sin(theta)
            #velocity from naive estimate v ~ sqrt(GMgalaxy/r)
            v = 4.738*np.exp(-r0/r)/np.sqrt(r)
            vx = -v*np.sin(theta)
            vy = v*np.cos(theta)
            # v = vx = vy = 0
            #generate body
            bodies.append(Body(m, rx, ry, vx=vx, vy=vy, L=L))
    #generate bar
    # refer to Ferrers 1877, Manos, Athanassoula 2011
    a = 6
    b = 1.5
    Nb = int(mb0/m)
    for i in range(Nb):
        #position from normalized distribution p(R) = (1/r0)exp(-r/r0)
        # rb = -rb0*np.log(1.0-np.random.rand())
        rb = r0
        if rb < rb0:
            theta = 2.0*np.pi*np.random.rand()
            # rbx = rb*np.cos(theta)
            rbx = 1.5 #kpc       
            rby = rb*np.sin(theta)
            alph = (rbx**2/a**2+rby**2/b**2)
            if alph < 1:
                    mb = mb0*(1-alph**2)**2
            elif alph >=1 :
                mb = 0.00001*mb0
            #velocity from naive estimate v ~ sqrt(GMgalaxy/r)
            # vb = 4.738*np.exp(-rb0/rb)/np.sqrt(rb)
            vb =  np.exp(-rb0/rb)/np.sqrt(rb)
            vbx = -vb*np.sin(theta)
            vby = vb*np.cos(theta)
            #generate body
            bodies.append(Body(mb, rbx, rby, vx=vbx, vy=vby, L=L, color = 'blue'))
    return bodies

#function: initialize array of bodies in uniform box
def generateUniform(rho, v0, N, L):
    #divide total among N masses
    m = rho*L**2/N
    #generate N bodies randomly distributed in box
    bodies = []
    for i in range(N):
        vx, vy = np.random.rand()*2*v0-v0, np.random.rand()*2*v0-v0
        rx, ry = np.random.rand()*2*L-L, np.random.rand()*2*L-L
        #generate body
        bodies.append(Body(m, rx, ry, vx=vx, vy=vy, L=L))
    return bodies
