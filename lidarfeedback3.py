#!/usr/bin/env python3

from lidar360 import Point, LidarKit
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import math

angle_maps = []
dist_maps = []

#matplotlib.use('tkagg')

time.sleep(1.0)
#Connect to the device
lk = LidarKit('/dev/ttyUSB0')

#Function to convert Polar to Cartisian
def polar_to_cart(a, d):
    x = d * math.cos((a+90) * math.pi / 180)
    y = d * math.sin((a+90) * math.pi / 180)
    return (x, y)

#Rotate for 360 degrees
lk.start()
time.sleep(1.0)

for j in range(0,10):

    #Creating 2 arrays to hold the x and y position of each poing
    points_angle = []
    points_dist = []
    #Coutning the number of points collected
    num_points = 0

    #Collect points if avaliable
    while not lk.points.empty():
        num_points += 1
        i = lk.points.get(0)

        #Ignore when distance is grater then 10 meters
        if i.dist > 10.0:
            continue

        #Get the Cartisian coordinates of the position of the points
        #x, y = polar_to_cart(i.angle, i.dist)
        #Add the new point to the array
        points_angle.append(i.angle)
        points_dist.append(i.dist)

        #print("[%d] %.2f deg @ %d ms" % (num_points, i.angle, i.timestamp))
    
    angle_maps.append(points_angle)
    dist_maps.append(points_dist)

    time.sleep(1)

# stop lidar
lk.stop()


#print("Number of points: %d" % num_points)

#fig, ax = plt.subplots()
#fig.set_figheight(15)
#fig.set_figwidth(15)

#Plot the lidar at (0, 0)
#plt.plot(0, 0, marker="o", markersize=8, markeredgecolor="red", 
#markerfacecolor="green")

#Plot the data points
#ax.scatter(points_x, points_y)

#plt.show()

for i in range(0,10):
    m = angle_maps[i]
    n = dist_maps[i]
    print("TRIAL %d" % (i+1))
    print(list(zip(m,n)))
    print("")
