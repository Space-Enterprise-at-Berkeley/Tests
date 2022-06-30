from packet import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import math

# -------------------------------------

def get_ranges(values):
    '''takes in a list of numerical values, and condenses any series of sequential
    values into tuples containing the first and last value of the series'''
    in_series = False
    ranges = []
    cur_start = 0
    for i, val in enumerate(values[:-1]):
        if values[i+1] == val + 1:  # if next val is sequential
            # if not in a series, mark val as start, otherwise continue to next check
            if not in_series:
                cur_start = val
                in_series = True
        else:                       # if next val is not sequential
            if in_series:
                ranges.append((cur_start,val))
                in_series = False
            else:
                ranges.append(val)
    if in_series:
        ranges.append((cur_start,values[-1]))
    return ranges

# -------------------------------------



# file = 'lad5_data.bin'
file = 'lad8/lad8_200000_byte_dump.bin'
# savefile = 'lad5_packets.pck'
savefile = 'lad8/lad8_blackbox.pck'

with open(file, 'rb') as f:
    data_bytes = f.read()

[]    
    
packets = []

idx = 0
report_thresh = 0
invalid_bytes = 0
invalid_indices = []
bitmap = [0]*len(data_bytes)
while idx < len(data_bytes):
    
    if idx > report_thresh:
        print(f"{report_thresh} bytes processed")
        report_thresh += 500
    
    id = data_bytes[idx]
    data_len = Packet.packetLen(id, 'inbound')
    
    # byte is not a valid id, try next byte
    if data_len == -1:
        # record invalid idx, and set as 1 in bitmap
        invalid_indices.append(idx)
        bitmap[idx] = 1
        idx += 1
        invalid_bytes += 1
        continue
    # byte is a valid id, test packet validity
    else:
        
        # break if have reached end of data_bytes
        if len(data_bytes[idx:idx+data_len]) < data_len:
            break
        
        p = Packet(raw_bytes=data_bytes[idx:idx+data_len])
        if p.is_valid:
            packets.append(p)
            idx += data_len
        else:
            # if checksum does not match, test next byte to see if it is a packet
            invalid_indices.append(idx)
            bitmap[idx] = 1
            idx += 1
            invalid_bytes += 1


trailing_bytes = [x for x in range(idx,len(data_bytes))]
invalid_indices.extend(trailing_bytes)

# if idx didn't end at last byte, add the trailing invalid bytes
invalid_bytes += len(trailing_bytes)
good_bytes = len(data_bytes) - invalid_bytes
print(f"{good_bytes} bytes successfully parsed as packets - {round(100*good_bytes/len(data_bytes),2)}%")
print(f"{invalid_bytes} bytes skipped during processing - {round(100*invalid_bytes/len(data_bytes),2)}%")
print(f"Writing {len(packets)} parsed packets to '{savefile}'")

toSave = [[len(data_bytes),good_bytes,invalid_bytes,invalid_indices],packets]

if savefile != '':
    with open(savefile, 'wb') as f:
        pickle.dump(toSave, f)
    
invalid_ranges = []
if len(invalid_indices) > 2:
    invalid_ranges = get_ranges(invalid_indices)


def byte_diff(x):
    if type(x) != tuple:
        return x
    else:
        return (x[1]-x[0]+1)
        
def byte_diff_id(x):
    if type(x) != tuple:
        return x
    else:
        return (x[1]-x[0]+1, data_bytes[x[0]])
    
# print(invalid_indices)
# print()
# print(invalid_ranges)
# print(list(map(byte_diff_id, invalid_ranges)))


zero_count = 0
zero_bytes = 0
zero_series_lengths = []
invalid_series_lens = []
for r in invalid_ranges:
    # only check for zero series r is a tuple, not just a single invalid byte
    if type(r) != int:
        data_range = data_bytes[r[0]:r[1]+1]
        invalid_series_lens.append(r[1]+1-r[0])
        if all([x == b'\x00' for x in data_range]):
            zero_count += 1
            zero_bytes += r[1]-r[0]+1
            # color bitmap pixels to show that is a series of zeros
            bitmap[r[0]:r[1]+1] = [0.5]*(r[1]-r[0]+1)
            zero_series_lengths.append(r[1]-r[0]+1)
    else:
        invalid_series_lens.append(1)


print(f"Of the {len(invalid_ranges)} ranges of invalid bytes, {zero_count} are straight zeros - {round(100*zero_bytes/invalid_bytes,2)}% of the invalid bytes")



display_dimension = math.ceil(math.sqrt(len(bitmap)))
bitmap += [0.2]*(display_dimension**2-len(bitmap)) # add filler bits at end if necessary
bitmap = np.array(bitmap)
bitmap_sq = bitmap.reshape(display_dimension, display_dimension)
plt.imshow(bitmap_sq)
plt.show()

raw_invalid_series_lens = invalid_series_lens
invalid_series_lens = [x for x in invalid_series_lens if x>1 and x <= 150]

plt.title('Invalid Series Length', fontsize=22)
plt.xlabel('Length (bytes)')
plt.ylabel('Count',fontsize=22)
bins = [x-0.5 for x in range(min(invalid_series_lens),max(invalid_series_lens)+2)]
plt.hist(invalid_series_lens, bins='auto', histtype='bar', ec='black')
plt.show()