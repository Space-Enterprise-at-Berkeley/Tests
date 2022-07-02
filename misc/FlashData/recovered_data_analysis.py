import pickle
import matplotlib.pyplot as plt
import numpy as np

from packet_defs import *


loadfile = 'lad8/lad8_blackbox.pck'
with open(loadfile, 'rb') as f:
    byte_info, packets = pickle.load(f)
    



base_time = packets[0].timestamp
# consider first packet as time=0, offset all subsequent packets accordingly
for p in packets:
    p.timestamp = (p.timestamp - base_time)/1000
    
# Report on overall recovered data
print(f"Num packets decoded: {len(packets)}")
print(f"Time range covered: {packets[-1].timestamp}s = {packets[-1].timestamp/60}m")
    
baro_t, baro_val = [], []
for p in packets:
    if p.id == 5:
        baro_t.append(p.timestamp)
        baro_val.append(p.data['baroAltitude'])
        

plt.plot(baro_t[:30], baro_val[:30])
plt.show()

baro_t = np.array(baro_t)

print("Baro Datarates")
datarate = []
t = 0
while t < baro_t[-1]:
    num_vals = len(baro_t[(baro_t >= t) & (baro_t < t+1)])
    print(num_vals)
    datarate.append(num_vals)
    t += 1
    
print("Avg Baro Datarate:", sum(datarate)/len(datarate))
datarate = np.array(datarate)


plt.title('Barometer Data Freq', fontsize=22)
plt.xlabel('Datarate (Hz)')
plt.ylabel('Count',fontsize=22)
sel_datarate = datarate[datarate > 0]
bins = [x-0.5 for x in range(min(sel_datarate),max(sel_datarate)+2)]

plt.hist(sel_datarate, bins=bins, histtype='bar', ec='black')
plt.show()
    
    
