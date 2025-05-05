#essential modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#essential imports
from Body import Body
from Quad import Quad
from BHTree import BHTree
from MCgalaxy import generateGalaxy
import os

#function: main
if __name__ == '__main__':
    #Milky Way parameters (default)
    r0 = 4.5 #kpc, scale length of galaxy
    rb0 = 5 #kpc, scale length of bar
    m0 = 5.0 #10^9 solar mass, mass of galaxy
    # mb0 = 20.0 #10^9 solar mass, mass of bar
    mb0 = 0.1*m0 #10^9 solar mass, mass of bar
    #simulation space
    N = 1000 #number of particles
    L = 150.0 #half length of box, kpc
    #Barnes-Hut simulation resolution
    theta = 1.0
    epsilon = theta*L/np.sqrt(N)
    #time evolution parameters
    dt = 1 #10Myr
    T = 250.0 #10Myr
    steps = int(T/dt)
    #generate 1000 masses in 15kpc box
    bodies = generateGalaxy(r0,rb0, m0, mb0, N, L)
    #generate Barnes-Hut tree on original grid
    tree = BHTree(Quad(-L,-L,2*L))
    #populate tree with bodies from list
    bod_dict = {}

    #make list of objects for plotting
    images = []
    #plotting setup
    fig = plt.figure()
    ax = plt.axes(xlim=(-L, L), ylim=(-L, L))
    #evolve N-body in time
    dict_time = []
    for i in range(steps):
        #computation counter
        print("Computing time step "+str(i+1)+"/"+str(steps))
        #generate Barnes-Hut tree on original grid
        tree = BHTree(Quad(-L,-L,2*L))
        #populate tree with bodies from list
        for body in bodies:
            tree.insertBody(body)
        #calculate force on every body from tree and evolve
        for body in bodies:
            body.resetForce()
            tree.applyForce(body, theta, epsilon)
            #take a time step
            t = dt*i
            body.update(dt)
        #append to list of objects for plotting
        position = np.array([body.r for body in bodies]).T
        velocities = np.array([body.v for body in bodies]).T
        for body in bodies:
            #calculate energy
            etot = np.array([body.Kenergy(dt)+body.Uinteract(body_1) if body_1!=body else body.Kenergy(dt) for body_1 in bodies]).T
        dict_time.append((etot, position, velocities))
        scatter, = ax.plot(position[0], position[1], 'k.')
        images.append((scatter,))
    

    orbit_data = {}
    
    for j in range(0,len(etot)):
        orb_x = []
        orb_y = []
        orb_vx = []
        orb_vy = []
        orb_z = []
        orb_vz = []
        t = []
        Etot = 0
        for i in range(0,len(dict_time)):
            etot, position, velocities = dict_time[i]
            Etot += etot[j]
            orb_x.append(position[0][j])
            orb_y.append(position[1][j])
            orb_z.append(0)
            orb_vx.append(velocities[0][j])
            orb_vy.append(velocities[1][j])
            orb_vz.append(0)
            t.append(i*dt)
        
        
        orbit_data[j] = (Etot, orb_x, orb_y,orb_z, orb_vx, orb_vy, orb_vz, t)
    print(t)
    # Create orbits directory if it doesn't exist
    os.makedirs("orbits", exist_ok=True)
    
    for key, data in orbit_data.items():
        Etot, x, y, z, vx, vy, vz, t = data
        with open(os.path.join("orbits", f"{key}.orb"), "w") as f:
            f.write(f"  {Etot}\n")
            dat = np.column_stack((t, x, y, z, vx, vy, vz))
            # print(dat)
            np.savetxt(f, dat, delimiter="  ")

    zoom = 1/8
    ax.set_xlim(-L*zoom, L*zoom)
    ax.set_ylim(-L*zoom, L*zoom)
    anim = animation.ArtistAnimation(fig, images, interval=100, blit=True)
    anim.save('BH-Nbody'+str(N)+'.mp4')
    plt.show()

    