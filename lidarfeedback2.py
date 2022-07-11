#!/usr/bin/env python3

from lidar360 import Point, LidarKit
import matplotlib.pyplot as plt
import numpy as np
import time
import math
import platform
from density import cluster_points

#plt.style.use('')

def polar_to_cart(a, d):
    x = d * math.cos((a+90) * math.pi / 180)
    y = d * math.sin((a+90) * math.pi / 180)
    return (x,y)

uri = ''
if platform.system() == 'Darwin':
    uri = '/dev/tty.usbserial-0001'
else:
    uri = '/dev/ttyUSB0'

time.sleep(1.0)
#lk = LidarKit('/dev/ttyUSB0')
#lk = LidarKit('/dev/tty.usbserial-0001')
lk = LidarKit(uri)
lk.start()
time.sleep(0.2)
lk.stop()

points = []
#points_x = []
#points_y = []
num_points = 0
while not lk.points.empty():
    num_points += 1
    i = lk.points.get(0)
    if i.dist > 15.0:
        continue
    x,y = polar_to_cart(i.angle, i.dist)
    #points_x.append(y)
    #points_y.append(x)
    points.append(np.array([x, y]))
    print("[%d] %.2f deg @ %d ms" % (num_points, i.angle, i.timestamp))

points_filtered = cluster_points(points, E=0.05, N=3)

p_x = [p[0] for p in points]
p_y = [p[1] for p in points]

pf_x = [p[0] for p in points_filtered]
pf_y = [p[1] for p in points_filtered]

print("Number of points: %d" % num_points)

fig, ax = plt.subplots()
#fig.set_figheight(15)
#fig.set_figwidth(15)
plt.plot(0, 0, marker="x", markersize=10, markeredgecolor="blue", markerfacecolor="blue")
ax.scatter(p_x, p_y, c="r")
ax.scatter(pf_x, pf_y, c="g")
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.show()
