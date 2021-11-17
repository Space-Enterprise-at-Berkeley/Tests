#!/usr/bin/env python
import math
import numpy as np
import time
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.animation as animation


tableAngle = 0
antennaAngle = 0

xpos, ypos, zpos = 0, 4, 4

pos = np.array([xpos,ypos,zpos])

tableAngle = math.atan(pos[1]/pos[0]) * 180/math.pi
horizontalLen = math.sqrt(xpos**2 + ypos**2)
antennaAngle = math.atan(pos[2]/horizontalLen) * 180/math.pi

print(f"Table Angle: {tableAngle}\nAntennaAngle: {antennaAngle}")


# ax.set_title("A line plot on a polar axis", va='bottom')
# plt.show()


angles = [x for x in range(0,361)]

r = np.arange(0, 1, 0.01)
theta = [angles[0]* math.pi/180] * len(r)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
line, = ax.plot(theta, r)

def update(num, r, angles, line):
    theta = [angles[num]* math.pi/180] * len(r)
    line.set_data(theta, r)
    return line,

ani = animation.FuncAnimation(fig, update, len(angles), fargs=[r, angles, line],
                              interval=25, blit=False)
plt.show()