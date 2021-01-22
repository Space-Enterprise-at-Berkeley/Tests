'''
FC.py - testing interface to Flight Computer

Goal: to create a command line script to connect with and send/receive messages
    to & from Eureka's Flight Computer

'''
import serial.tools.list_ports
import serial

class SerialConn:
    def __init__(self):
        pass


    def openConnection(self):
        """List the current serial ports and either use user input or a saved
        previous selection to select and open one of the listed serial ports."""
        pass

    def sendData(self):
        pass

    def readLine(self):
        pass


    def __savePort(self):
        """Save the current port being used to a file so that it can be resued
        later without needing user input selection."""

        pass

    def readPort(self):
        """Read and return the last saved port."""

        pass


class FlightComputer:
    def __init__(self):
        pass

    def setHighPressureSolenoid(self,state):
        pass

    def setLoxGems(self,state):
        pass

    def setPropGems(self,state):
        pass

    def setMainArm(self,state):
        pass

    def setLoxMain(self,state):
        pass

    def setPropMain(self,state):
        pass
