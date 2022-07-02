import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from copy import deepcopy
from scipy import interpolate
import time
'''
Set of functions that help in processing data from influxDB
'''




def get_event_time(events, event_name):
    return events[events == event_name].index[0]

def offset_index_time(dataFrameDict, timeOffset, series=False):
    '''Takes a dictionary of dataframes, which have timestamps as their indices,
    and subtracts the timeOfsset from all timestamps in each dataFrame, making
    the index relative to the timeOffset. Converts each timedelta into seconds.

    Args:
        dataFrameDict: dictionary of dataframes, where each dataFrame has as its index datetimes.
        timeOffset: must be a full datetime.

    Returns:
        Nothing
    '''
    # if series, package as dataframe
    if series:
        dataFrameDict = {'blah':dataFrameDict}
    for key in dataFrameDict.keys():
        # perform subtraction on entire index, then convert the resulting list
        # of time deltas into a list of time values in seconds
        dataFrameDict[key].index = list(map(lambda x: x.total_seconds(), dataFrameDict[key].index - timeOffset))

def influx_str(timestamp, offset=0):
    '''Takes a panda datetime object and returns it as a string that is compatible with
    influx query language. Can optionally add an offset to the given timestamp

    Args:
        timestamp: (?) a pandas datetime
        offset: an int or float number of seconds by which to offset the given timestamp.

    Returns:
        Nothing
    '''

    if offset > 0:
        timestamp = timestamp + pd.Timedelta(offset,'s')
    elif offset < 0:
        timestamp = timestamp - pd.Timedelta(abs(offset),'s')
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def graph_channel(df, start=None, end=None, show=False, plot=True):
    '''Graphs some crap

    '''
    # Create default of all True
    start_vals = df.index == df.index
    end_vals = df.index == df.index

    # Override if a value is passed in
    if start:
        start_vals = df.index > start
    if end:
        end_vals = df.index < end

    index_vals = start_vals & end_vals
    to_graph = df[index_vals]

    if plot:

        plt.plot(to_graph.index, to_graph['value'])

        if show:
            plt.show()

    else:
        return to_graph
    
def removeDuplicates(events, time_resolution=0.005):
    index = events.index
    for i in reversed(range(len(index) - 1)):
        t1, t2 = index[i], index[i+1]
        # check if timestamp 2 is within time_resolution of timestamp 1
        if t1 + pd.Timedelta(time_resolution,'s') > t2:
            events.drop(t2, inplace=True)
            
def getGroupings(events, max_spacing=5):
    index = events.index
    groupings = [{'times':[index[0]], 'text':[events[index[0]]]}]
    run_index = 0
    for i in range(len(index) - 1):
        t1, t2 = index[i], index[i+1]
        if t1 + pd.Timedelta(max_spacing, 's') > t2:
            groupings[run_index]['times'].append(t2)
            groupings[run_index]['text'].append(events[t2])
        else:
            groupings.append({'times':[t2], 'text':[events[t2]]})
            run_index += 1
    return [pd.Series(data=x['text'], index=x['times']) for x in groupings if len(x['times']) > 1]
    
    
def in_grouping(group, event):
    '''Returns True if EVENT is present in GROUP (a fcEvent grouping produced by getGroupings() )
        
    '''
    return any([event==x for x in group])