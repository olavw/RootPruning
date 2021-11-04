import serial
import time

baudrate = 38400
usbPort = 'COM4'  # set the correct port before run it

gpsRead = serial.Serial(port=usbPort, baudrate=baudrate, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
gpsRead.timeout = 2  # set read timeout
# print gpsRead  # debug serial.
print(gpsRead.is_open)  # True for opened
if gpsRead.is_open:
    while True:
        size = gpsRead.inWaiting()
        if size:
            data = gpsRead.read(size)
            print(data)
        else:
            print('no data')
        time.sleep(1)
else:
    print('gpsRead not open')
# z1serial.close()  # close z1serial if z1serial is open.