import re
import time
import csv

import urllib3
urllib3.disable_warnings()

from influxdb import InfluxDBClient

client = InfluxDBClient('influx.andycate.com', 443, 'waterflowClient', 'waterflowClient', 'misc', ssl=True, verify_ssl=False)


with open('Eggtimer_FlightData.csv', newline='') as f:
     reader = csv.reader(f)
     num = 0
     for row in reader:
         if num == 0:
            num += 1
            continue
         points = [{
                "measurement": "eggy2",
                "tags": {},
                "fields": {"T": float(row[0]),
                        "Alt": float(row[1]),
                        "Veloc": float(row[2]),
                        "AccelG": float(row[3]),
                        "AccelFPSS": float(row[4]),
                        "VAccel": float(row[5]),
                        "AltAccel": float(row[6]),
                        "Filt_Alt": float(row[7]),
                        "FVeloc": float(row[8]),
                        "FAccelG": float(row[9]),
                        "FAccelFPSS": float(row[10]),
                        "FAccelVel": float(row[11]),
                        "FAccelAlt": float(row[12]),
                        "LDA": float(row[13]),
                        "MaxV": float(row[14]),
                        "MaxA": float(row[15]),
                        "BO#1": float(row[16]),
                        "LowV": float(row[17]),
                        "Apogee": float(row[18]),
                        "N-O": float(row[19]),
                        "CH2": float(row[20]),
                        "CH5": float(row[21]),}
                }]
         client.write_points(points)
