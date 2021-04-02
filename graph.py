import matplotlib.pyplot as plt
import numpy as np
import re

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
imu_orientation = [x, y, z]

with open('smth.txt') as f:
    while line:
        line = f.readline()[1:-1]
        data = re.split(r",|\|")
        id = int(line[0])
        if id == 2:
            voltage.append(float(data[1]))
            power.append(float(data[2])])
            current_draw.append(float(data[3]))
        if id == 5:
            num_pkts_sent.append(float(data[1]))
        if id == 10:
            drogue.append(float(data[1]))
            main.append(float(data[2]))
        if id == 11:
            lat.append(float(data[1]))
            lon.append(float(data[2]))
        if id == 12:
            fix.append(float(data[1]))
            num_sat.append(float(data[2]))
            alt.append(float(data[3]))
            speed.append(float(data[4]))
            angle.append(float(data[5]))
        if id == 13:
            altitude.append(float(data[1]))
            pressure.append(float(data[2]))
        if id == 14:
            accel_x.append(float(data[1]))
            accel_y.append(float(data[2]))
            accel_z.append(float(data[3]))
        if id == 15:
            x.append(float(data[1]))
            y.append(float(data[2]))
            z.append(float(data[3]))

plt.plot(voltage, label = 'voltage')
plt.plot(power, label = 'power')
plt.plot(current_draw, label = 'current draw')
plt.savefig("batterystats.png")
np.save("batterystats.npy", np.array(batterystats))
np.load("batterystats.npy")

plt.plot(num_pkts_sent, label = '# packets sent')
plt.savefig("numpktssent.png")
np.save("numpktssent.npy", np.array(num_pkts_sent))
np.load("numpktssent.npy")

plt.plot(drogue, label = 'drogue')
plt.plot(main, label = 'main')
plt.savefig("recoveryack.png")
np.save("recoveryack.npy", np.array(recovery_ack))
np.load("recoveryack.npy")

plt.plot(lat, label = 'latitude')
plt.plot(lon, label = 'longitude')
plt.savefig("gps.png")
np.save("gps.npy", np.array(gps))
np.load("gps.npy")

plt.plot(fix, label = 'fix')
plt.plot(num_sat, label = 'num sat')
plt.plot(alt, label = 'alt')
plt.plot(speed, label = 'speed')
plt.plot(angle, label = 'angle')
plt.savefig("gpsaux.png")
np.save("gpsaux.npy", np.array(gps_aux))
np.load("gpsaux.npy")

plt.plot(altitude, label = 'altitude')
plt.plot(pressure, label = 'pressure')
plt.savefig("barometer.png")
np.save("barometer.npy", np.array(barometer))
np.load("barometer.npy")

plt.plot(accel_x, label = 'accel x')
plt.plot(accel_y, label = 'accel y')
plt.plot(accel_z, label = 'accel z')
plt.savefig("imuaccel.png")
np.save("imuaccel.npy", np.array(imu_accel))
np.load("imuaccel.npy")
 
plt.plot(x, label = 'x')
plt.plot(y, label = 'y')
plt.plot(z, label = 'z')
plt.savefig("imuorientation.png")
np.save("imuorientation.npy", np.array(imu_orientation))
np.load("imuorientation.npy")
