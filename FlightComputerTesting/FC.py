'''
FC.py - testing interface to Flight Computer

Goal: to create a command line script to connect with and send/receive messages
    to & from Eureka's Flight Computer

'''
import serial.tools.list_ports
import serial

from packet import *

_DEBUG = 0

def debug(level, msg):
    if _DEBUG >= level:
        print(msg)

class SerialConn:
    def __init__(self):
        self.ser = None
        pass


    def openConnection(self):
        """List the current serial ports and either use user input or a saved
        previous selection to select and open one of the listed serial ports."""
        print("Initializing")
        chosenCom = ""
        ports = list(serial.tools.list_ports.comports())
        for i, p in enumerate(ports):
            print("{0}: {1}".format(i+1,p))
            if "Arduino" in p.description or "ACM" in p.description or "cu.usbmodem" in p[0]:
                chosenCom = p[0]
                print("Chosen COM: {}".format(p))
        if not chosenCom:
            self.stop_thread("No Valid Com Found")
            return
        print("Chosen COM {}".format(chosenCom))
        baudrate = 57600
        print("Baud Rate {}".format(baudrate))
        try:
            ser = serial.Serial(chosenCom, baudrate,timeout=3)
            self.ser = ser
        except Exception as e:
            self.stop_thread("Invalid Serial Connection")
            return
        ser.flushInput()


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

s = SerialConn()
s.openConnection()
fc = FlightComputer(s)
