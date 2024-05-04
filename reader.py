import serial

ADDRESS = '/dev/tty.usbmodem2101'
BAUDRATE = 115200



ser = serial.Serial(ADDRESS, BAUDRATE, timeout=0.1)         # 1/timeout is the frequency at which the port is read

while True:
    data = ser.readline().decode().strip()
    if data:
        print(data)

