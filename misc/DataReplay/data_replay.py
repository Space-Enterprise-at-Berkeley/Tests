from influxdb import DataFrameClient
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from copy import deepcopy
from scipy import interpolate
import time
from influx_helpers import *




def define_update(dframe, ax, line, start, fin, interval, win_length=3, ramp_up=False):
    '''Does a thing

    Args

    Returns:
        a function!
    '''

    win_start = start - win_length
    win_end = start

    def update(frame):
        nonlocal dframe, win_start, win_end, win_length, ramp_up
        t_delta = interval/1000.0

        win_mask = (dframe.index > win_start) & (dframe.index < win_end)

        print(win_start, win_end, len(dframe[win_mask]))

        to_graph = graph_channel(dframe,win_start,win_end,show=False,plot=False)

        line.set_data(to_graph.index, to_graph['value'])

        # recompute the ax.dataLim
        ax.relim()
        # update ax.viewLim using the new dataLim
        ax.autoscale_view()


        if ramp_up:
            win_end += t_delta

            if win_end - win_start >= win_length:
                ramp_up = False
                win_end = win_start + win_length
        else:
            win_start += t_delta
            win_end += t_delta

        return line,

    return update


def define_frame_gen(total_time, interval):
    '''

    Args:

    Returns:
        A function
    '''

    frame_num = round((total_time) / (interval/1000.0))
    print(f"Total Frames: {frame_num}")
    if frame_num < 0:
        raise ValueError(f"Stop time must be after start time. Got a start time of {start_time} and stop time of {stop_time}")

    def frame_gen():
        i = 0
        start = time.time()
        print(frame_num)
        while i <= frame_num:
            if i == frame_num-1:
                end = time.time()
                duration = end-start
                print(f"Generated {i+1} frames in {round(duration,2)} seconds")
                print(f"Framerate of {round((i+1)/duration,2)}")
            yield i
            i += 1


    return frame_gen


def create_data_replay(data, start, stop, title, ylabel, file_name, speed_factor=1, xlabel='Time (s)', frames=60, fixed_scale=None):

    # TODO: Check that data has a time based index and 'value' column
    # TODO: Check that the start & stop times are valid for the timestamps of the given data
    # TODO: Check that file_name has '.mp4' as extension

    ylabel_mappings = {
        'psi' : 'Pressure (psi)',
        'degc' : 'Temp (ºC)',
        'degc' : 'Temp (ºF)',
        'current' : 'Current (A)',
        'current-m' : 'Current (mA)',
        'volt' : 'Voltage (V)',
        'volt-m' : 'Voltage (mV)',
        'kg': 'Thrust (kg)',
        'alt': 'Altitude (m)'
    }

    clip_length = stop - start


    # 16.66667 is interval in ms for 60 fps
    # interval = (1000/frames)*speed_factor
    interval = 16.6666666667*speed_factor

    fig, ax = plt.subplots()

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel_mappings[ylabel])
    
    if fixed_scale:
        print("TESTING")
        ax.set_ylim([min(min(data['value']),0), max(data['value'])*1.1])

    frame_num = clip_length / (interval/1000.0)

    ani = animation.FuncAnimation(
        fig,
        define_update(data, ax, line, start, stop, interval),
        frames=define_frame_gen(clip_length,interval),
        repeat=False, interval=1, blit=True, save_count=frame_num)

    
    ani.save(file_name, fps=speed_factor*1/(interval/1000.0))
