from datetime import datetime

def parseDate(date):
    ''' parse datetime of format 1/30/2021 5:29:53.676000000 PM '''
    date = date.split(' ')
    date[0] = list(map(int,date[0].split('/'))) # split into day, month, year
    date[0] = [date[0][2], date[0][0], date[0][1]] # month, day, year -> year, month, day
    date[1] = date[1].split(':') # split into hour, minute, seconds
    timestamp = [int(date[1][0]), int(date[1][1])]
    sec, micsec = date[1][2].split('.')
    micsec = int(float('0.' + micsec)*1000000) #convert to integer microseconds
    timestamp.extend([int(sec), micsec])
    if date[2].upper() == 'PM':
        timestamp[0] += 12
    res = date[0] + timestamp
    d = datetime(*res)
    return d.timestamp()



with open("LOX.csv", 'r') as f:
    raw_data = f.readlines()
    data = list(map(lambda x: float(x.split(',')[1]), raw_data[1:]))
    times = list(map(lambda x: parseDate(x.split(',')[0]), raw_data[1:]))


deltas = []
for i in range(len(times)-1):
    deltas.append(1000*(times[i+1]-times[i])) #difference between each timestamp in ms

print("Avg Delay: {0:.1f}ms".format(sum(deltas)/len(deltas)))

setVals = list(data)

max = 1000
for i, val in enumerate(setVals):
    if val >= 0:
        setVals[i] = int((val/1000)*4096)
    else:
        setVals[i] = 0
    setVals[i] += 410 #offset for base of 0.5V

i = 0
print('{')
line = ''
for val in setVals:
    line += str(val) + ', '
    i += 1
    if i == 8:
        print(line)
        line = ''
        i = 0
if i != 0:
    print(line[:-1])
print('};')

print(len(setVals))
