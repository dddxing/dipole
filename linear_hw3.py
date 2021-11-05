from vpython import *
import numpy as np
from math import pi

global g, T, dt, k_floor

mass_init = [[2, 4, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 5]] # [[p1x, p1y, p1z, v1x, v1y, v1z, a1x, a1y, a1z, m1],[]]
spring_init = [[10000, 2]] # [[k1, l1o]]

g = vector(0, -9.81, 0)
# g = -9.81
F_ext = vector(0,0,0) #external force

dt = 0.0001
k_floor = 1000

def make_axes(length):
    global axes
    xaxis = arrow(pos=vector(0,1,0),axis=vector(length,0,0),color=color.red)
    yaxis = arrow(pos=vector(0,1,0),axis=vector(0,length,0),color=color.green)
    zaxis = arrow(pos=vector(0,1,0),axis=vector(0,0,length),color=color.blue)
    fudge = 0.06*length
    xlabel = label(text="x",color=xaxis.color,pos=xaxis.pos+xaxis.axis+vector(0,fudge,0),box=False)
    ylabel = label(text="y",color=yaxis.color,pos=yaxis.pos+yaxis.axis+vector(fudge,0,0),box=False)
    zlabel = label(text="z",color=zaxis.color,pos=zaxis.pos+zaxis.axis+vector(fudge,0,0),box=False)
    return 

def create_floor():
    floor = box(pos=vector(0,0,0), size = vector(10, 0.25, 10), color = color.blue, texture=textures.rough)
    return floor


def main():
    axis = make_axes(1)
    floor = create_floor()

    # storing mass and spring objects
    m = []
    s = []

    # loop through mass_init to create the spheres
    for mass in mass_init:
        m.append(sphere(pos=vector(mass[0], mass[1], mass[2]), color=color.green, radius=0.3, vel=vector(mass[3], mass[4], mass[5]), accel=vector(mass[6], mass[7], mass[8]), force=vector(mass[6], mass[7], mass[8]), m=mass[9]))

    for spring in spring_init:
        for i in range(len(m)):
            for j in range(i+1, len(m)):

                # getting dist btw two points 
                dist = sqrt((m[i].pos.x - m[j].pos.x) ** 2 + (m[i].pos.y - m[j].pos.y) ** 2+ (m[i].pos.z - m[j].pos.z) ** 2)
                
                # getting scalar spring force
                force_scalar = spring[0]* (dist-spring[1])
                
                # getting direction of the spring force
                F_spring_dir = norm(m[i].pos - m[j].pos)
                
                s.append(curve([m[i].pos, m[j].pos], color=color.red, radius=0.1, k=spring[0], l0=spring[1], force=force_scalar*F_spring_dir, nodeA=m[i], nodeB=m[j]))
    T = 0
    while T < 10000:

        rate(1/dt)

        for mass in m:
            for spring in s:
                # adding spring force from both end
                if spring.nodeA == mass:
                    mass.force += spring.force
                if spring.nodeB == mass:
                    mass.force += spring.force
            
            # adding gravity and external force
            mass.force = mass.m * g + F_ext
            
            dz = mass.pos.y - (floor.pos.y + floor.size.y + 2 * mass.radius)

            # checking if mass is below floor level
            if dz < 0:
                force_floor = vector(0, -k_floor * dz, 0)
                mass.force += force_floor

        for mass in m:

            mass.accel = mass.force / mass.m
            mass.vel += mass.accel * dt
            mass.pos += mass.vel * dt
            

        # loop through springs and update connections
        for spring in s:
            dist = sqrt((spring.nodeA.pos.x - spring.nodeB.pos.x) ** 2 + (spring.nodeA.pos.y - spring.nodeB.pos.y) ** 2+ (spring.nodeA.pos.z - spring.nodeB.pos.z) ** 2)
            force_scalar = spring.k * (dist- spring.l0)
            F_spring_dir = norm(spring.nodeA.pos - spring.nodeB.pos)
            spring.force = F_spring_dir * force_scalar
            for i in range(0, len(m)):
                for j in range(i+1, len(m)):
                    spring.modify(0, m[i].pos)
                    spring.modify(1, m[j].pos)


        if T % 100 == 0:
            print(f"pos = {m[0].pos}" )
        T += dt


if __name__ == "__main__":

    main()

