import numpy as np
import matplotlib.pyplot as plt

TERMINAL_VELOCITY = -20
g = -9.8
DELTA_T = 20e-3

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
    for j in range(len(data)):
        x, P = predict(x, P)
        curr_measurement = data[j]
        x, P, K = update(curr_measurement, x, P)
        filtered.append(x)
    return np.asarray(filtered)

'''
    Convenient way to plot out Alt, Vel & Acceleration.
'''
def plot_states(time, state, state_2=None, apogee=None):
    # Index when v = 0 for time array
    actualApogee = 0
    start_i = 0
    end_i = len(time)

    altitude = state[:, 0, 0]
    velocity = state[:, 1, 0]
    accel = state[:, 2, 0]

    if(apogee is not None):
        start_i = apogee - 150
        end_i = apogee + 150

    if(state_2 is not None):
        altitude_2 = state_2[:, 0, 0]
        velocity_2 = state_2[:, 1, 0]
        accel_2 = state_2[:, 2, 0]
        actualApogee = actApogee(state_2)
    
    print(start_i)
    print(end_i)
    plt.plot(time[start_i:end_i], altitude[start_i:end_i])
    plt.xlabel("time (s)")
    plt.ylabel("height (m)")
    if(state_2 is not None):
        plt.plot(time[start_i:end_i], altitude_2[start_i:end_i])
        plt.axvline(time[actualApogee], color='yellow', label="Actual Apogee")
    if(apogee is not None):
        plt.axvline(time[apogee], label='Approx. Apogee')
    plt.legend()
    plt.show()

    plt.plot(time[start_i:end_i], velocity[start_i:end_i])
    plt.xlabel("time (s)")
    plt.ylabel("velocity (m/s)")
    plt.axhline(0)
    if(state_2 is not None):
        plt.plot(time[start_i:end_i], velocity_2[start_i:end_i])    
        plt.axvline(time[actualApogee], color='yellow', label="Actual Apogee")
    if(apogee is not None):
        plt.axvline(time[apogee], label='Approx. Apogee')
    plt.legend()
    plt.show()

    plt.plot(time[start_i:end_i], accel[start_i:end_i])
    plt.xlabel("time (s)")
    plt.ylabel("accel ($\\frac{m}{s^2}$)")
    if(state_2 is not None):
        plt.plot(time[start_i:end_i], accel_2[start_i:end_i])
        plt.axvline(time[actualApogee], color='yellow', label="Actual Apogee")
    if(apogee is not None):
        plt.axvline(time[apogee], label='Approx. Apogee')
    plt.legend()
    plt.show()

    if(apogee is not None and state_2 is not None):
        apogee_diff = round(time[apogee] - time[actualApogee], 4)
        print('Actual - Approx Apogee = ' + str(apogee_diff) + '(s)')


def descending(data, index_around, region_of_interest=5):
    '''
    index_around: index around which to check if we are descending
    region_of_interest: how far back to look

    returns:
        bool
    '''
    descending = True
    for i in range(index_around - region_of_interest, index_around):
        descending &= (data[i] > data[i + 1])
    return descending


def Apogee(filtered_data):
    '''
    Return the index of data point where it believes apogee is based on descending function above.
    @var: OUTLOOK determines how many time-steps back the descending function has to look back to check if we are descending.
    
    returns: 
        int
    '''
    height_data = filtered_data[:,0,0]

    outlook = 15
    for i in range(outlook, len(height_data)):
        if(descending(height_data, i, outlook)):
            return i
    return -1

def actApogee(filtered_data):
    '''
    Returns the index where velocity is closest to zero.

    returns:
        int
    '''
    data = filtered_data[:,0,0].tolist()
    return data.index(max(data))