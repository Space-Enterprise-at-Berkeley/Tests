import time
from packet import *

import pytest

#----------------Helpers-----------------

def gen_basic_packet():
    raw_bytes = b''
    
    raw_bytes += b'\x03' # add ID of 3
    raw_bytes += b'\x0c' # add data len of 12 bytes
    raw_bytes += b'\x64\x00\x00\x00' # add timestamp of 100 milliseconds since start
    raw_bytes += b'\xaa\x13' # add a checksum
    raw_bytes += b'\xec\x51\x40\x41' # data 1
    raw_bytes += b'\x9a\x99\x99\x3f' # data 2
    raw_bytes += b'\xb4\xc8\x66\x41' # data 3
    
    return raw_bytes

#-----------------Tests------------------

def test_blank():
    p = Packet()
    
def test_bad_id():
    with pytest.raises(Exception):
        p = Packet(-1, []) # no negative IDs
    
def test_wrong_data_len():
    with pytest.raises(Exception):
        p = Packet(0, []) # 0 is a valid ID, with a non-zero data field
        
def test_good_data_len():
    packetDef = outboundPackets[0]
    p = Packet(0, [4]*len(packetDef))
    
def test_id_only():
    pass # TODO
    
def test_data_only():
    pass # TODO
    
def test_wrong_types():
    pass # TODO
    
def test_num_bytes():
    pass # TODO
    
def test_packet_decode():
    raw_bytes = gen_basic_packet()
    p = Packet(raw_bytes=raw_bytes)
    
def test_packet_encode():
    time.sleep(0.321)
    p = Packet(id=3, data=[1,2,3], pack_type='inbound')
    p.encode()
    
def test_packet_loopback():
    time.sleep(0.321)
    p_send = Packet(id=3, data=[1,2,3], pack_type='inbound')
    raw_bytes = p_send.encode()
    
    p_recv = Packet(raw_bytes=raw_bytes)
    print(p_recv.full_str())
    
    
    
    
    
if __name__ == '__main__':
    test_packet_loopback()