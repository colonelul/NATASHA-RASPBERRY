import serial

def sendData(inputVal):
    if __name__=='__main__':
        ser = serial.Serial('/dev/ttyACM0',9600, timeout=1)
        ser.flush()
        ser.write(b"on\n")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)