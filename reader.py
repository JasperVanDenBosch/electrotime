import serial
from datetime import datetime
import numpy

ADDRESS = '/dev/tty.usbmodem2101'
BAUDRATE = 115200
dt_str = datetime.now().isoformat().replace(':', '').replace(' ', '-').split('.')[0]
fpath = f'data/latrec_{dt_str}.npy'

lines = []

ser = serial.Serial(ADDRESS, BAUDRATE, timeout=5)         # 1/timeout is the frequency at which the port is read
ser.flush()

for _ in range(400_000): ## number of data points. Each about .9ms. 1m34s? 
    line = ser.readline().decode().strip()
    if line:
        lines.append(line)

print(f'Finished recording. Re-structuring data..')

rows = []
epoch_nr = 0
for line in lines:
    if 'reset' in line:
        epoch_nr += 1
    else:
        cells = line.split(' ')
        rows.append([epoch_nr]+[int(c) for c in cells])
data = numpy.asarray(rows, dtype=numpy.uint16)
numpy.save(fpath, data)

print(f'Saved data as {fpath}')

