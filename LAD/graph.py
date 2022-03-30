import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
​
voltage = []
power = []
current_draw = []
battery_stats = [voltage, power, current_draw]

num_pkts_sent = []

drogue = []
main = []
recovery_ack = [drogue, main]

lat = []
lon = []
gps = [lat, lon]

fix = []
num_sat = []
alt = []
speed = []
angle = []
gps_aux = [fix, num_sat, alt, speed, angle]

altitude = []
pressure = []
barometer = [altitude, pressure]

accel_x = []
accel_y = []
accel_z = []
imu_accel = [accel_x, accel_y, accel_z]

x = []
y = []
z = []

timestamps = []
imu_orientation = [x, y, z]
columns = ['timestamp', 'voltage', 'power', 'current_draw', 'num_pkts_sent', 'drogue', 'main', 'lat', 'lon', 'fix', 'num_sat', 'alt', 
          'speed', 'angle', 'altitude', 'pressure', 'accel_x', 'accel_y', 'accel_z', 'x', 'y', 'z']
len(columns)
f = [0] + [None]*21
f

rows = []

with open('LAD4_1 (1).txt') as f:
    # go through each line
    # split
    # if we reach a new timestamp
    # copy over all values
    # go through current timestamp and replace with new values'
    legend_line = f.readline()
    lines = f.readlines()
    for line in lines:
        line = line.replace(' ', '')
        line = line.split('|')[0]
        line = line.replace('{', '')
        data = line.split(",")
        timestamp = float(data[0]) #timestamp is milliseconds (int)
        row = [timestamp] +[None]*21
        id = int(data[1])
        if id == 2:
            row[1] = float(data[2]) # voltage
            row[2] = float(data[3]) # power
            row[3] = float(data[4]) # current draw
        if id == 5:
            row[4] = float(data[2]) # nm packets sent
        if id == 10:
            row[5] = float(data[2]) #drogue
            row[6] = float(data[3]) 
        if id == 11:
            row[7] = float(data[2])
            row[8] = float(data[3])
        if id == 12:
            row[9] = float(data[2])
            row[10] = float(data[3])
            row[11] = float(data[4])
            row[12] = float(data[5])
            row[13] = float(data[6])
        if id == 13:
            row[14] = float(data[2])
            row[15] = float(data[3])
        if id == 14:
            row[16] = float(data[2])
            row[17] = float(data[3])
            row[18] = float(data[4])
        if id == 15:
            row[19] = float(data[2])
            row[20] = float(data[3])
            row[21] = float(data[4])
        rows.append(row)
            
dataframe = pd.DataFrame(rows, columns=columns)
dataframe

dataframe = dataframe.fillna(method='ffill').fillna(0)
dataframe

plt.plot(dataframe['timestamp'], dataframe['voltage'], label = 'voltage')
plt.plot(dataframe['timestamp'], dataframe['power'], label = 'power')
plt.plot(dataframe['timestamp'], dataframe['current_draw'], label = 'current draw')
plt.legend()
plt.savefig("batterystats.png")
np.save("batterystats.npy", np.array([dataframe['voltage'], dataframe['power'], dataframe['current_draw']
]))
np.load("batterystats.npy")

plt.plot(dataframe['timestamp'], dataframe['num_pkts_sent'], label = '# packets sent')
plt.legend()
plt.savefig("numpktssent.png")
np.save("numpktssent.npy", np.array(dataframe['num_pkts_sent']))
np.load("numpktssent.npy")

plt.plot(dataframe['timestamp'], dataframe['drogue'], label = 'drogue')
plt.plot(dataframe['timestamp'], dataframe['main'], label = 'main')
plt.legend()
plt.savefig("recoveryack.png")
np.save("recoveryack.npy", np.array([dataframe['drogue'], dataframe['main']]))
np.load("recoveryack.npy")

plt.plot(dataframe['timestamp'], dataframe['lat'], label = 'latitude')
plt.plot(dataframe['timestamp'], dataframe['lon'], label = 'longitude')
plt.legend()
plt.savefig("gps.png")
np.save("gps.npy", np.array([dataframe['lat'], dataframe['lon']]))
np.load("gps.npy")

plt.plot(dataframe['timestamp'], dataframe['altitude'], label = 'altitude')
plt.plot(dataframe['timestamp'], dataframe['pressure'], label = 'pressure')
plt.legend()
plt.savefig("barometer.png")
np.save("barometer.npy", np.array([dataframe['altitude'], dataframe['pressure']]))
np.load("barometer.npy")

plt.plot(dataframe['timestamp'], dataframe['accel_x'], label = 'accel x')
plt.plot(dataframe['timestamp'], dataframe['accel_y'], label = 'accel y')
plt.plot(dataframe['timestamp'], dataframe['accel_z'], label = 'accel z')
plt.legend()
plt.savefig("imuaccel.png")
np.save("imuaccel.npy", np.array([dataframe['accel_x'], dataframe['accel_y'], dataframe['accel_z']]))
np.load("imuaccel.npy")

plt.plot(dataframe['timestamp'], dataframe['x'], label = 'x')
plt.plot(dataframe['timestamp'], dataframe['y'], label = 'y')
plt.plot(dataframe['timestamp'], dataframe['z'], label = 'z')
plt.legend()
plt.savefig("imuorientation.png")
np.save("imuorientation.npy", np.array([dataframe['x'], dataframe['y'], dataframe['z']]))
np.load("imuorientation.npy")
