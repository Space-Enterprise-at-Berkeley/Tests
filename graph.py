import matplotlib.pyplot as plt
import numpy as np

with open('smth.txt') as f:
    line = f.readline()
    while line:
        line = f.readline()
        line.split(",")

lox_pt_temp = [
    lox_tree = []
    lox_heater = []]
    if line[0][1] == 0:
        lox_tree.append(line[1])
        lox_heater.append(line[2])

all_pressures = [
    lox_tank = []
    prop_tank = []
    lox_inj = []
    prop_inj = []
    pressurant = []
    lox_dome = []
    prop_dome = []
    lox_gems = []]
    if line[0][1] == 1:
        lox_tank.append(line[1])
        prop_tank.append(line[2])
        lox_inj.append(line[3])
        prop_inj.append(line[4])
        pressurant.append(line[5])
        lox_dome.append(line[6])
        prop_dome.append(line[7])
        lox_gems.append(line[8])

battery_stats = [
    voltage = []
    power = []
    current_draw = []]
    if line[0][1] == 2:
        voltage.append(line[1])
        power.append(line[2])
        current_draw.append(line[3])

load_cell = [
    input1 =[]
    input2 =[]]
    if line[0][1] == 3:
        input1.append(line[1])
        input2.append(line[2])

cryo_temps = [
    cryo_lox_tank = []
    cryo_inj_1 =[]
    lox_adapter_tree_pt = []
    lox_gems_ct = []
    if line[0][1] == 4:
        cryo_lox_tank.append(line[1])
        cryo_inj_1.append(line[2])
        lox_adapter_tree_pt.append(line[3])
        lox_gems_ct.append(line[4])

num_pkts_sent = []
    if line[0][1] == 5:
        num_pkts_sent.append(line[1])

lox_gems_temp = [
    lox_gems_temp = []
    lox_gems_heater = []]
    if line[0][1] == 6:
        lox_gems_temp.append(line[1])
        lox_gems_heater.append(line[2])

endflow_detection_case = []
    if line[0][1] == 7:
        endflow_detection_case.append(line[1])

recovery_ack = [
    drogue = []
    main = []]
    if line[0][1:3] == 10:
        drogue.append(line[1])
        main.append(line[2])
gps = [
    lat = []
    lon = []]
    if line[0][1:3] == 11:
        lat.append(line[1])
        lon.append(line[2])

gps_aux = [
    fix = []
    num_sat = []
    alt = []
    speed = []
    angle = []]
    if line[0][1:3] == 12:
        fix.append(line[1])
        num_sat.append(line[2])
        alt.append(line[3])
        speed.append(line[4])
        angle.append(line[5])

barometer = [
    altitude = []
    pressure = []]
    if line[0][1:3] == 13:
        altitude.append(line[1])
        pressure.append(line[2])
imu_accel = [
    accel_x = []
    accel_y = []
    accel_z = []]
    if line[0][1:3] == 14:
        accel_x.append(line[1])
        accel_y.append(line[2])
        accel_z.append(line[3])

imu_orientation() = [
    x = []
    y = []
    z = []]
    if line[0][1:3] == 15:
        x.append(line[1])
        y.append(line[2])
        z.append(line[3])

# x, y = np.loadtxt('smth.txt', delimiter=',', unpack=True)
# plt.plot(x,y, label='Loaded from file!')

# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('smth')
# plt.legend()
# plt.show()