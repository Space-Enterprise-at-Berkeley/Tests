import math
import numpy as np
import matplotlib.pyplot as plt


tableAngle = 0
antennaAngle = 0

xpos, ypos, zpos = 0, 4, 4

pos = np.array([xpos,ypos,zpos])

tableAngle = math.atan(pos[1]/pos[0]) * 180/math.pi
horizontalLen = math.sqrt(xpos**2 + ypos**2)
antennaAngle = math.atan(pos[2]/horizontalLen) * 180/math.pi

print(f"Table Angle: {tableAngle}\nAntennaAngle: {antennaAngle}")



