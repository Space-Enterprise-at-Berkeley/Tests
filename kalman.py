import numpy as np
import matplotlib.pyplot as plt

TERMINAL_VELOCITY = -20
g = -9.8
DELTA_T = 1e-3  # interval in seconds

x = np.matrix([[0.],  # pos
               [1.],  # velocity
               [2.]])  # accel

F = np.matrix([[1, DELTA_T, DELTA_T**2 / 2],  # state transition matrix
               [0, 1, DELTA_T],
               [0, 0, 1]])

sigma_b = 0.5  # barometer
sigma_a = 0.5  # accelerometer

R = np.matrix([[sigma_b**2, 0],
               [0, sigma_a**2]])

# vector of measured data
m = np.matrix([[0],  # position
               [0]])  # acceleration

# maps true variable to measured data
H = np.matrix([[1, 0, 0],
               [0, 0, 1]])

B = np.matrix([[0],
               [0],
               [1]])

Q = np.matrix([[0, 0, 0],
               [0, 0, 0],
               [0, 0, 1]])


def predict(x, P):
    x = F@x  # u_k = 0, init x[3] = -g
    P = F@P@F.T + Q
    return x, P


def update(z, x, P):
    y = z - H@x
    S = H@P@H.T + R
    K = P@H.T@S.I
    x = x + K@y
    P = (np.identity(3) - K@H)@P
    return x, P, K


def kalman(data):
    '''
    * data is an array of measurement vector of size 2x1
    '''
    filtered = []
    x = np.matrix([[0],
                   [0],
                   [0]])
    P = np.identity(3)
    for j in range(len(data) - 1):
        x, P = predict(x, P)
        curr_measurement = data[j]
        x, P, K = update(curr_measurement, x, P)
        filtered.append(x)
    return np.asarray(filtered)


def plot_states(time, state, start_i, end_i, state_2=None, apogee=None):

    altitude = state[:, 0, 0]
    velocity = state[:, 1, 0]
    accel = state[:, 2, 0]

    if(state_2 is not None):
        altitude_2 = state_2[:, 0, 0]
        velocity_2 = state_2[:, 1, 0]
        accel_2 = state_2[:, 2, 0]

    plt.plot(time[start_i:end_i], altitude[start_i:end_i])
    plt.xlabel("time (s)")
    plt.ylabel("height (m)")
    if(state_2 is not None):
        plt.plot(time[start_i:end_i], altitude_2[start_i:end_i])
    if(apogee is not None):
        plt.axvline(apogee)
    plt.show()

    plt.plot(time[start_i:end_i], velocity[start_i:end_i])
    plt.xlabel("time (s)")
    plt.ylabel("velocity (m/s)")
    plt.axhline(0)
    if(state_2 is not None):
        plt.plot(time[start_i:end_i], velocity_2[start_i:end_i])
    if(apogee is not None):
        plt.axvline(apogee)
    plt.show()

    plt.plot(time[start_i:end_i], accel[start_i:end_i])
    plt.xlabel("time (s)")
    plt.ylabel("accel ($\\frac{m}{s^2}$)")
    if(state_2 is not None):
        plt.plot(time[start_i:end_i], accel_2[start_i:end_i])
    if(apogee is not None):
        plt.axvline(apogee)
    plt.show()


def descending(data, index_around, region_of_interest=5):
    '''
    index_around: index around which to check if we are descending
    region_of_interest: how far back to look

    returns:
        bool
    '''
    descending = True
    for i in range(index_around - region_of_interest, index_around):
        descending &= data[i] > data[i + 1]
    return descending


def Apogee(filtered_data):
    outlook = 100
    for i in range(outlook, len(filtered_data)):
        if(descending(filtered_data, i, outlook)):
            return i
    return -1
