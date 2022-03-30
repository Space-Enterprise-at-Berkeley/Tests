import struct
from datetime import datetime
import math

from packet_defs import *

'''
TODO:
    - change general exceptions to more specific exceptions
'''

class Packet:
    
    
    initTime = datetime.now()
    header_fmt = '<BBIH' # format string for id, len, runTime, & checksum
    header_fmt_no_chck = '<BBI' # without checksum, so can be used to calculate checksum
    header_len = struct.calcsize(header_fmt)
    
    
    def packetLen(id, pack_type):
        pack_type = pack_type.lower()
        if pack_type not in ['inbound', 'outbound']:
            return -1
            
        # id 0 is commit hash, length is unknown
        if id == 0:
            return -1
        
        if pack_type == 'inbound':
            packetList = inboundPackets
        else:
            packetList = outboundPackets
            
        if id not in packetList:
            return -1
        
        packetDef = packetList[id]
        data_fmt, data_len = Packet.gen_data_fmt(packetDef, pack_type)
        
        return data_len + Packet.header_len
        
            
    def gen_data_fmt(packetDef, pack_type):
        data_fmt = '<'        
        for item in packetDef:
            if pack_type == 'outbound':
                dtype = item
            elif pack_type == 'inbound':
                dtype = item[1]
            
            data_fmt += fmtMappings[dtype]
        data_len = struct.calcsize(data_fmt)
        return data_fmt, data_len
    
    
    def __init__(self, id = None, data = None, raw_bytes = None, pack_type=''):
        self.raw_data = None
        self.data = None
        self.id = None
        self.data_len = None # num bytes of data
        self.timestamp = None
        self.checksum = None
        self.is_valid = False
        self.err_str = "Invalid Packet! "
        pack_type = pack_type.lower()
        self.pack_type=pack_type
        
        
        
        if id and raw_bytes:
            err_str = "Error! Cannot pass in both an ID to create an outgoing "
            err_str += " packet and a bytearray to parse an incoming packet " 
            raise Exception(err_str)
        
        # if ID is provided, check ID against OUTBOUND packet definition
        if id != None:
            # if pack_type has not been specified, use default of outbound
            if len(pack_type) == 0:
                self.pack_type = 'outbound'
                
            if self.pack_type == 'outbound':
                packetList = outboundPackets
            elif self.pack_type == 'inbound':
                packetList = inboundPackets
            else:
                pass
                
            if data != None:
                    
                    
                
                if id not in packetList.keys():
                    err_str = f"Error! Cannot find ID '{id}' in packet definition: {self.pack_type}Packets"
                    raise Exception(err_str)
                    
                packetDef = packetList[id]
                
                if len(data) != len(packetDef):
                    err_str = f"Error! {pack_type.capitalize()} packet ID:{id} expected {len(packetDef)} data values "
                    err_str += f"(got {len(data)})"
                    raise Exception(err_str)
                    
                self.id = id
                self.packetDef = packetDef
                self.data = data
                self.packetList = packetList
                
                self.is_valid = True
                
        
        # if bytes is provided, parse it into a packet
        if raw_bytes != None:
            
            # if pack_type has not been specified, use default of inbound
            if len(pack_type) == 0:
                self.pack_type = 'inbound'
                
            if self.pack_type == 'outbound':
                self.packetList = outboundPackets
            elif self.pack_type == 'inbound':
                self.packetList = inboundPackets
            else:
                pass
            
            # size of packet header is 8
            if len(raw_bytes) < Packet.header_len:
                raise Exception(f"Packet has min size of {Packet.header_len} bytes, only got {len(raw_bytes)}")
            else:
                self.decode_data(raw_bytes)
                
        # struct.pack("f", val)

    def get_id(self):
        return self.sensor_id

    def get_data(self):
        return self.data

    def get_sum(self):
        return self.checksum

    def is_valid(self):
        return True
        
    def addInt8(self, val):
        pass
        
    def addFloat(self, val):
        pass
        
    def parse(val):
        pass
        
        
    def encode(self):
        ''' 
        Takes in a list of data values and a packetDef and returns a bytearray
        
            Parameters:
                    data (list): A list of data values
                    packetDef (list): A parallel list of datatypes for each item
                        in the data list

            Returns:
                    byte_data (str): byte array produced by applying types to 
                        each data value
        
        '''
        if len(self.data) != len(self.packetDef):
            raise Exception("Data lengths does not match length of packet definition")
            
        bytes_out = b''
            
        data_fmt, data_len = Packet.gen_data_fmt(self.packetDef, self.pack_type)
        self.data_len = data_len
            
        time_elapsed = math.floor((datetime.now()-Packet.initTime).total_seconds()*1000)
        hdr_no_check_bytes = struct.pack(Packet.header_fmt_no_chck, self.id, data_len, time_elapsed )
        
        data_bytes = struct.pack(data_fmt, *self.data)
        
        # calculate checksum
        self.checksum = fletcher16(hdr_no_check_bytes + data_bytes)
        self.time_elapsed = time_elapsed
        check_bytes = struct.pack("<H", self.checksum)
        
        return hdr_no_check_bytes + check_bytes + data_bytes
        
        
            
        pass
        
    def decode_data(self, raw_bytes):
        ''' 
        Takes in a list of data values and a packetDef and returns a bytearray
        
        Packet format:
        [ ________ | ________ | ________ ________ ________ ________ | ________ ________ | ________ ... ________ ]
        [    id    |   len    |              runTime                |       checkSum    |          data         ]
        [  u_int8  |  u_int8  |              u_int32                |        u_int16    |     defined in doc    ]
        
            Parameters:
                    data (list): A list of data values
                    packetDef (list): A parallel list of datatypes for each item
                        in the data list

            Returns:
                    byte_data (str): byte array produced by applying types to 
                        each data value
        
        '''
        
        names = []
        
        id, data_len, timestamp, checksum = struct.unpack(Packet.header_fmt, raw_bytes[:8])
        
        if id not in self.packetList:
            self.is_valid = False
            self.err_str += f"ID:{id} not found in packet definition {self.pack_type}Packets"
            return False
            
        packetDef = inboundPackets[id]
        
        data_fmt = '<' # use little endian encoding
        for item in packetDef:
            name, dtype = item
            data_fmt += fmtMappings[dtype]
            names.append(name)
        
        # check that packet definition size matches read data_len
        if struct.calcsize(data_fmt) != data_len:
            self.err_str += f"Expected {struct.calcsize(data_fmt)} bytes of data for packet (received data length of {data_len})"
            self.is_valid = False
            return False
        
        # check that checksum matches
        if checksum != fletcher16(raw_bytes[0:6] + raw_bytes[8:]):
            # print(self.checksum, fletcher16(raw_bytes[0:6] + raw_bytes[8:]))  
            self.err_str += f"Received and calculated checksums did not math. "
            self.is_valid = False
            return False
        
        # if all checks pass, then packet is valid
        self.is_valid = True
            
        # unpack data
        data_vals = struct.unpack_from(data_fmt, raw_bytes, offset=Packet.header_len)
        self.data = {}
        for i, name in enumerate(names):
            self.data[name] = data_vals[i]
            self.data[i] = data_vals[i]
            
        self.id = id
        self.data_len = data_len
        self.timestamp = timestamp
        self.checksum = checksum
        
    def full_str(self):
        if self.is_valid:
            # divide len by 2 because there are string and numerical keys
            data_str = ','.join(map(str, [round(self.data[i],3) for i in range(len(self.data)//2)]))
            return f"{{{self.id},{self.data_len},{self.timestamp},{self.checksum},{data_str}}}"
        else:
            return self.err_str
            
    def __str__(self):
        if self.is_valid:
            if type(self.data) == dict:
                num_data = len(self.data)//2
            else:
                num_data = len(self.data)
            # divide len by 2 because there are string and numerical keys
            data_str = ','.join(map(str, [round(self.data[i],3) for i in range(num_data)]))
            return f"{{{self.id},{data_str}}}"
        else:
            return self.err_str
            
    def __repr__(self):
        if self.is_valid:
            return f"{{{self.id},{self.timestamp}}}"
        else:
            return {'invalid'}
        
def fletcher16(raw_bytes):
    
    sum1 = 0
    sum2 = 0
    # converts string into an array of bytes for easy math
    for byte in raw_bytes:
        sum1 = (sum1 + byte) % 256
        sum2 = (sum1 + sum2) % 256
    return sum2 << 8 | sum1
