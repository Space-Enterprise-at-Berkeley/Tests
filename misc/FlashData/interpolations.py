from enum import Enum

class DataType(Enum):
    FLOAT = 0
    UINT8 = 1
    UINT16 = 2
    UINT32 = 3
    
fmtMappings = {
    DataType.FLOAT:'f',
    DataType.UINT8:'B',
    DataType.UINT16:'H',
    DataType.UINT32:'I'
}    


'''
Follow format string convention define here:
https://docs.python.org/3/library/struct.html
'''

def asFloat(val, symb=False):
    if val == None:
        return "f"
    else:
        return val
        
    
def asASCIIString(raw_bytes, symb=False):
    if symb:
        return '??'
    else:
        return raw_bytes.decode('utf8')

def asUInt8(val, symb=False):
    if val == None:
        return "B"
    else:
        return val
        
        
def asUInt16(val, symb=False):
    if val == None:
        return "H"
    else:
        return val
        
    
def asUInt32(val, symb=False):
    if val == None:
        return "I"
    else:
        return val
        
    