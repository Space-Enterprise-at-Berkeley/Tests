'''
FC.py - testing interface to Flight Computer

Goal: to create a command line script to connect with and send/receive messages
    to & from Eureka's Flight Computer

'''
import serial.tools.list_ports
import serial

import argparse

from packet import *

_DEBUG = 0

def debug(level, msg):
    if _DEBUG >= level:
        print(msg)

class SerialConn:
    def __init__(self, debug=False):
        self.ser = None
        self.debug = debug


    def openConnection(self):
        """List the current serial ports and either use user input or a saved
        previous selection to select and open one of the listed serial ports."""
        print("Initializing")
        chosenCom = ""
        ports = list(serial.tools.list_ports.comports())
        for i, p in enumerate(ports):
            if self.debug:
                print("{0}: {1}".format(i+1,p))
            if "Arduino" in p.description or "ACM" in p.description or "cu.usbmodem" in p[0]:
                chosenCom = p[0]
                print("Chosen Serial Port: {}".format(p))
        if not chosenCom:
            print("SerialConn Error: No Valid Serial Port Found.")
            return False
        print("Chosen COM {}".format(chosenCom))
        baudrate = 57600
        print("Baud Rate {}".format(baudrate))
        try:
            ser = serial.Serial(chosenCom, baudrate,timeout=3)
            self.ser = ser
        except Exception as e:
            print("SerialConn Error: Unable to open Serial Connection")
            return False
        ser.flushInput()
        return True


    def sendData(self, msg):
        bytes = (str(msg) + "\r\n").encode('utf-8')
        if self.ser is not None:
            self.ser.write(bytes)
        pass

    def readLine(self):
        if self.ser is not None:
            return str(self.ser.readline())
        else:
            return ''


    def __savePort(self):
        """Save the current port being used to a file so that it can be resued
        later without needing user input selection."""

        pass

    def readPort(self):
        """Read and return the last saved port."""

        pass


class FlightComputer:
    def __init__(self, conn=None):
        self.conn = conn
        self.serial = True
        pass

    def setHighPressureSolenoid(self,state):
        self.write(26, [state])

    def setLoxGems(self,state):
        self.write(22, [state])

    def setPropGems(self,state):
        self.write(25, [state])

    def setMainArm(self,state):
        self.write(20, [state])

    def setLoxMain(self,state):
        self.write(21, [state])

    def setPropMain(self,state):
        self.write(24, [state])

    def write(self, id, data):
        if self.serial:
            writeSerial(id, data)
            

    def writeSerial(self, id, data):
        pack = Packet(data, id=id)
        try:
            print(pack.encoded_message)
            if self.conn is not None:
                self.conn.sendData(pack.encoded_message)
        except Exception as e:
            print("Write error")
            return False
        return True

    def read(self):
        pass
        # pack = Packet(rawData)

def main(args):
    s = SerialConn()
    if s.openConnection():
        fc = FlightComputer(s)
    else:
        return

    if args.lox_gems:
        fc.setLoxGems(args.lox_gems)
    elif args.lox_main:
        fc.setLoxGems(args.lox_main)
    elif args.prop_gems:
        fc.setPropGems(args.prop_gems)
    elif args.lox_main:
        fc.setPropGems(args.prop_main)
    elif args.arm:
        fc.setMainArm(args.arm)
    elif args.high_pressure_solenoid:
        fc.setHighPressureSolenoid(args.high_pressure_solenoid)






if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Configuration
    # parser.add_argument('--set_port', type=str,
    #                     help='set default port to be used when connecting to Flight Computer')

    # Flight Computer Commands
    parser.add_argument('-lg', '--lox_gems', type=int, choices=[0, 1],
                        help='Open or Close LOX GEMS (relief valve)')
    parser.add_argument('-lm', '--lox_main', type=int, choices=[0, 1],
                        help='Open or Close LOX Main Valve')
    parser.add_argument('-pg', '--prop_gems', type=int, choices=[0, 1],
                        help='Open or Close Propane GEMS (relief valve)')
    parser.add_argument('-pm', '--prop_main', type=int, choices=[0, 1],
                        help='Open or Close Propane Main Valve')
    parser.add_argument('-a', '--arm', type=int, choices=[0, 1],
                        help='Open or Close Arming Valve')
    parser.add_argument('-hps', '--high_pressure_solenoid', type=int, choices=[0, 1],
                        help='Open or Close High Pressure Solenoid')
    args = parser.parse_args()
    main(args)
