from vpython import *
import numpy as np
from math import pi

global g, T, dt, k_floor

# mass_init = [
#             [2, 4, 0, 0, 0, 0, 0, 0, 0, 0.8],
#             [0, 2, 0, 0, 0, 0, 0, 0, 0, 0.8],
#             [0, 6, 2, 0, 0, 0, 0, 0, 0, 0.8]] # [[p1x, p1y, p1z, v1x, v1y, v1z, a1x, a1y, a1z, m1],[]]
x=3
height = 3
side = 1
mass_init = [
                [x, x, x, 0, 0, 0, 0, 0, 0, 0.8],
                [x+1, x, x, 0, 0, 0, 0, 0, 0, 0.8],
                [x, x+1, x, 0, 0, 0, 0, 0, 0, 0.8],
                [x, x, x+1, 0, 0, 0, 0, 0, 0, 0.8],
                [x+1, x+1, x, 0, 0, 0, 0, 0, 0, 0.8],
                [x+1, x, x+1, 0, 0, 0, 0, 0, 0, 0.8],
                [x, x+1, x+1, 0, 0, 0, 0, 0, 0, 0.8],
                [x+1, x+1, x+1, 0, 0, 0, 0, 0, 0, 0.8]]

spring_const_default = 10
spring_length_default = 2
spring_init = []
for i in range(len(mass_init)):
    for j in range(i+1, len(mass_init)):
        dist = sqrt((mass_init[i][0] - mass_init[j][0]) ** 2 + (mass_init[i][1] - mass_init[j][1]) ** 2 + (mass_init[i][2] - mass_init[j][2]) ** 2)
        # if dist < sqrt(2):
        # dist = spring_length_default
        spring_init.append([spring_const_default, dist])

# g = vector(0, -98.1, 0)
g = vector(0, -9.81, 0) 
F_ext = vector(0,0,0) #external force
damping_coefficent = 0.9
dt = 0.01
k_floor = 10000

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
    floor = box(pos=vector(0,0,0), size = vector(20, 0.25, 20), color = color.blue)
    return floor


def main():
    # axis = make_axes(1)
    floor = create_floor()

    # storing mass and spring objects
    m = []
    s = []

    # loop through mass_init to create the spheres
    for mass in mass_init:
        m.append(sphere(pos=vector(mass[0], mass[1], mass[2]), color=color.green, radius=0.1, vel=vector(mass[3], mass[4], mass[5]), accel=vector(mass[6], mass[7], mass[8]), force=vector(mass[6], mass[7], mass[8]), m=mass[9]))

    for spring in spring_init:
        for i in range(len(m)):
            for j in range(i+1, len(m)):

                # initilizing dist btw two points 

                dist = mag(m[i].pos - m[j].pos)
                
                # initilizing scalar spring force
                force_scalar = spring[0] * (dist - spring[1])
                
                # initilizing direction of the spring force
                F_spring_dir = norm(m[i].pos - m[j].pos)
                # F_spring_dir = (m[i].pos - m[j].pos) / dist
                # calculate the spring force vector using direction and scalar
                F_spring = force_scalar * F_spring_dir
                # if dist <= sqrt(2):
                s.append(curve([m[i].pos, m[j].pos], color=color.red, radius=0.05, k=spring[0], l0=spring[1], force=F_spring, nodeA=m[i], nodeB=m[j]))

    T = 0
    i = 1
    while i < 100000:
        # from IPython import embed; embed()
        rate(1000)

        for mass in m:

            for spring in s:
                # adding spring force from both ends
                if spring.nodeA == mass:
                    mass.force -= spring.force

                if spring.nodeB == mass:
                    mass.force += spring.force
            
            # adding gravity and external force
            mass.force += mass.m * g + F_ext
            # print(mass.force)
            
            dz = mass.pos.y - (floor.pos.y + floor.size.y + 1 * mass.radius)
            
            # checking if mass is below floor level
            if dz < 0:
                force_floor = vector(0, -k_floor * dz, 0)
                mass.force += force_floor

        for mass in m:
            # print(f"force: {mass.force}")
            mass.accel = mass.force / mass.m
            # print(f"accel: {mass.accel}")
            mass.vel = mass.vel * damping_coefficent + mass.accel * dt
            # print(f"vel: {mass.vel}")
            mass.pos += mass.vel * dt

            
            # mass.force = vector(0, 0, 0)
            

        # loop through springs and update connections
        for spring in s:
            for mass in m:
                if spring.nodeA == mass:
                    spring.modify(0, mass.pos, visible=1)
                if spring.nodeB == mass:
                    spring.modify(1, mass.pos, visible=1)
                mass.force = vector(0, 0, 0)


            dist = mag(spring.nodeA.pos - spring.nodeB.pos)
            
            force_scalar = spring.k * (dist- spring.l0)
            F_spring_dir = norm(spring.nodeA.pos - spring.nodeB.pos)
            # F_spring_dir = (spring.nodeA.pos - spring.nodeB.pos) / dist
            spring.force = F_spring_dir * force_scalar


        # if T % 100 == 0:
        # print(f"pos = {m[0].pos}" )
        # T += dt
        i += 1


if __name__ == "__main__":

    main()

