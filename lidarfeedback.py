#!/usr/bin/env python3

from lidar360 import Point, LidarKit
import matplotlib.pyplot as plt
import numpy as np
import time
import math

#plt.style.use('')

def polar_to_cart(a, d):
    x = d * math.cos((a+90) * math.pi / 180)
    y = d * math.sin((a+90) * math.pi / 180)
    return (x,y)

time.sleep(1.0)
lk = LidarKit('/dev/ttyUSB0')
lk.start()
time.sleep(1.0)
lk.stop()

points_x = []
points_y = []
num_points = 0
while not lk.points.empty():
    num_points += 1
    i = lk.points.get(0)
    if i.dist > 10.0:
        continue
    x,y = polar_to_cart(i.angle, i.dist)
    points_x.append(y)
    points_y.append(x)
    print("[%d] %.2f deg @ %d ms" % (num_points, i.angle, i.timestamp))

print("Number of points: %d" % num_points)

fig, ax = plt.subplots()
fig.set_figheight(15)
fig.set_figwidth(15)
plt.plot(0, 0, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
ax.scatter(points_x, points_y)
#plt.xlim(-0.5,0.5)
#plt.ylim(-0.5,0.5)
plt.show()
