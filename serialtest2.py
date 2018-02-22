import serial

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout =3.0)
count = 0
while True:
    count = count + 1
    port.write("A")
    read = port.readline()
    print (str(count))+(" character received: ")+ (read)