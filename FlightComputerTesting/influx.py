import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from time import sleep
import os
import scipy as sc
from numpy.fft import rfft, irfft
from scipy import signal
from scipy.signal import savgol_filter, lfilter
from statistics import mean
from scipy.interpolate import interp1d
from influxdb import InfluxDBClient

import json

from config import *

target_db = 'misc'
i_creds = {}
i_creds['usr'] = 'waterflowClient'
i_creds['pwd'] = 'waterflowClient'

client = InfluxDBClient('influx.andycate.com', 443, i_creds['usr'], i_creds['pwd'], target_db, ssl=True)

json_body = [
    {
        "measurement": "test",
        "tags": {
            "recording" : "test",
            "type" : "fake"
        },
        "fields": {
            "value": 3
        }
    }
    ]

# client.write_points(json_body)





# data = client.query("select value from \"propTank\" where recording = 'waterflow1'")
# rawTimes, values = get_data(data)
# time = extractSeconds(rawTimes)
