import serial
from datetime import datetime

ADDRESS = '/dev/tty.usbmodem2101'
BAUDRATE = 115200
dt_str = datetime.now().isoformat().replace(':', '').replace(' ', '-').split('.')[0]
fpath = f'data/latrec_{dt_str}.txt'

lines = []

ser = serial.Serial(ADDRESS, BAUDRATE, timeout=5)         # 1/timeout is the frequency at which the port is read
ser.flush()

for i in range(100_000): ## number of data points. Each about .9ms. 1m34s? 
    line = ser.readline().decode().strip()
    if line:
        lines.append(line)
    if i % 1000 == 0:
        print(f'data point {i/1000} x1000')

print(f'Finished recording. Re-structuring data..')

with open(fpath, 'w') as fhandle:
    fhandle.writelines('\n'.join(lines))

print(f'Saved data as {fpath}')

