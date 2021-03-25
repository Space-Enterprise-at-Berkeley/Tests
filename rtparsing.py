import serial
import serial.tools.list_ports

import re
import time

from influxdb import InfluxDBClient
import urllib3
urllib3.disable_warnings()

ser = serial.Serial("/dev/cu.usbserial-AB0KTZ91", 57600)

class SerialConnection:

    def __init__(self, debug=False):
        self.ser = None
        self.debug = debug

    def enter_mode(self):
        ser.write(str("+++").encode("utf-8"))
        print(ser.readline())
        return True

    def get_data(self):
        ser.write(str("ATI7\r\n").encode("utf-8"))
        ser.readline()
        response = ser.readline().decode("utf-8")
        print(response)
        return Response(response)
            
class Response:

    def __init__(self, name):
        self.name = name

    def left_rssi(self):
        patn = r'[a-zA-Z/ ]+', 'L/R RSSI'
        return int(re.search(r'L\/R RSSI: (\d+)\/(\d+)', self.name).group(1))

    def right_rssi(self):
        patn = r'[a-zA-Z/ ]+', 'L/R RSSI'
        return int(re.search(r'L\/R RSSI: (\d+)\/(\d+)', self.name).group(2))
    
    def left_noise(self):
        patn = r'[a-zA-Z/ ]+', 'L/R noise'
        return int(re.search(r'L\/R noise: (\d+)\/(\d+)', self.name).group(1))

    def right_noise(self):
        patn = r'[a-zA-Z/ ]+', 'L/R noise'
        return int(re.search(r'L\/R noise: (\d+)\/(\d+)', self.name).group(2))
        
    def pkts(self):
        patn = r'[a-zA-Z/ ]+', 'pkts'
        return int(re.search(r'pkts: (\d+)', self.name).group(1))

    def txe(self):
        patn = r'[a-zA-Z/ ]+', 'txe'
        return int(re.search(r'txe=(\d+)', self.name).group(1))

    def rxe(self):
        patn = r'[a-zA-Z/ ]+', 'rxe'
        return int(re.search(r'rxe=(\d+)', self.name).group(1))

    def stx(self):
        patn = r'[a-zA-Z/ ]+', 'stx'
        return int(re.search(r'stx=(\d+)', self.name).group(1))

    def srx(self):
        patn = r'[a-zA-Z/ ]+', 'srx'
        return int(re.search(r'srx=(\d+)', self.name).group(1))

    def ecc1(self):
        patn = r'[a-zA-Z/ ]+', 'ecc'
        return int(re.search(r'ecc=(\d+)\/(\d+)', self.name).group(1))
        
    def ecc2(self):
        patn = r'[a-zA-Z/ ]+', 'ecc'
        return int(re.search(r'ecc=(\d+)\/(\d+)', self.name).group(2))

    def temp(self):
        patn = r'[a-zA-Z/ ]+', 'temp'
        return int(re.search(r'temp=(^-\d+$)', self.name).group(1))

    def dco(self):
        patn = r'[a-zA-Z/ ]+', 'dco'
        return int(re.search(r'dco=(\d+)', self.name).group(1))

client = InfluxDBClient('influx.andycate.com', 443, 'waterflowClient', 'waterflowClient', 'misc', ssl=True, verify_ssl=False)

s = SerialConnection()
s.enter_mode()
while True:
    r = s.get_data()
    print(r.left_rssi())
    points = [{
            "measurement": "radio2",
            "tags": {},
            "fields": {"left_rssi": r.left_rssi(),
                "right_rssi": r.right_rssi(),
                "left_noise": r.left_noise(),
                "right_noise": r.right_noise(),
                "pkts": r.pkts(),
                "rxe": r.rxe(),
                "stx": r.stx(),
                "srx": r.srx(),
                "ecc1": r.ecc1(),
                "ecc2": r.ecc2(),
                "temp": r.temp(),
                "dco": r.dco()}
        }]
    client.write_points(points)
    time.sleep(1)