import pickle
import matplotlib.pyplot as plt
import numpy as np


loadfile = 'lad5_packets.pck'
with open(loadfile, 'rb') as f:
    byte_info, packets = pickle.load(f)
    



base_time = packets[0].timestamp
for p in packets:
    p.timestamp = (p.timestamp - base_time)/1000
    
print(packets)


baro_t, baro_val = [], []
for p in packets:
    if p.id == 5:
        baro_t.append(p.timestamp)
        baro_val.append(p.data['baroAltitude'])
        

# plt.plot(baro_t, baro_val)

# plt.show()

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
    
    
