#!/usr/bin/env python3

from lidar360 import Point, LidarKit
import matplotlib.pyplot as plt
matplotlib.use('GTKAgg')
import numpy as np
import time
import math

time.sleep(1.0)
#Connect to the device
lk = LidarKit('/dev/ttyUSB0')
#Rotate for 360 degrees
lk.start()
time.sleep(1.0)
lk.stop()

#Creating 2 arrays to hold the x and y position of each poing
points_x = []
points_y = []
#Coutning the number of points collected
num_points = 0

#Function to convert Polar to Cartisian
def polar_to_cart(a, d):
    x = d * math.cos((a+90) * math.pi / 180)
    y = d * math.sin((a+90) * math.pi / 180)
    return (x, y)

#Collect points if avaliable
while not lk.points.empty():
    num_points += 1
    i = lk.points.get(0)
    
    #Ignore when distance is grater then 10 meters
    if i.dist > 10.0:
        continue
        
    #Get the Cartisian coordinates of the position of the points
    x, y = polar_to_cart(i.angle, i.dist)
    #Add the new point to the array
    points_x.append(y)
    points_y.append(x)
    
    print("[%d] %.2f deg @ %d ms" % (num_points, i.angle, i.timestamp))

print("Number of points: %d" % num_points)

fig, ax = plt.subplots()
fig.set_figheight(15)
fig.set_figwidth(15)

#Plot the lidar at (0, 0)
plt.plot(0, 0, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="green")
#Plot the data points
ax.scatter(points_x, points_y)

plt.show()
