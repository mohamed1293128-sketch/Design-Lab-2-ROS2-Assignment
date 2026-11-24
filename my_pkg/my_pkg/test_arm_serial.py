import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)

while True:
  command = input('Base, Shoulder: ')

  if command == 'q':
    break

  ser.write((command + '\n').encode())
  print(ser.readline().decode().strip())

ser.close()