#! /usr/bin/python3
import threading
import serial
import socket
from serial.tools import list_ports
import time
import json

def ser_to_soc(ser, soc, port):
    pac = ''
    while True:
        b = ser.read(1).decode('utf-8')
        # print('yeet')
        if b == '\n':
            # print('kms')
            soc.sendto(pac.encode('utf-8'), ('10.0.0.69', port))
            soc.sendto(pac.encode('utf-8'), ('10.0.0.70', port))
            pac = ''
        else:
            pac += b

def soc_to_influx(ser, soc):
    while True:
        data, addr = soc.recvfrom(1024)
        
        ser.write(data);


def main():


    port_info = {
    'AC1': {
            'ser_obj': None,
            'soc': None,
            'port_num': 42069
        },
    'AC2': {
            'ser_obj': None,
            'soc': None,
            'port_num': 42070
        },
    'AC3': {
            'ser_obj': None,
            'soc': None,
            'port_num': 42071
        }
    }

    for ser_port in open_ser_ports:
        if ser_port.name in ['ttyACM0','ttyACM1','ttyACM2']:
            ac_str = ac_ser_nums[get_ser_num(ser_port)]
            port_info[ac_str]['ser_obj'] = serial.Serial(
                port=f'/dev/{ser_port.name}',
                baudrate=57600)
            port_info[ac_str]['soc'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            port_info[ac_str]['soc'].bind(('0.0.0.0', port_info[ac_str]['port_num']))

    print(port_info)

    for ac_str in port_info.keys():
        if port_info[ac_str]['ser_obj'] is not None:
            ser = port_info[ac_str]['ser_obj']
            soc = port_info[ac_str]['soc']

            print(f"Starting {ac_str} send to port {port_info[ac_str]['port_num']}")
            ser_to_soc_t = threading.Thread(target=ser_to_soc, args=(ser, soc, port_info[ac_str]['port_num']))
            ser_to_soc_t.start()

            print(f"Starting {ac_str} receive on port {port_info[ac_str]['port_num']}")
            soc_to_ser_t = threading.Thread(target=soc_to_ser, args=(ser, soc))
            soc_to_ser_t.start()

    while True:
        time.sleep(1000) # forever

if __name__ == '__main__':
    main()
