import serial

ser = serial.Serial("/dev/serial0", 115200, timeout=1)
print("✅ Listening on /dev/serial0 ...")

while True:
    data = ser.readline()
    if data:
        print("RAW:", data)
