import serial
from datetime import datetime

ADDRESS = '/dev/tty.usbmodem2101'
BAUDRATE = 115200
fname = datetime.now().isoformat().replace(':', '').replace(' ', '-')

lines = []

ser = serial.Serial(ADDRESS, BAUDRATE, timeout=5)         # 1/timeout is the frequency at which the port is read

for _ in range(10_000):
    line = ser.readline().decode().strip()
    if line:
        lines.append(line)


with open(f'{fname}.txt', 'w') as fhandle:
    fhandle.write('\n'.join(lines))


