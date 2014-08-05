#!/usr/bin/python
import sys
import os
import serial
import socket

try : 
  SerialPort = serial.Serial('/dev/ttyACM0', 9600)
  SerialPort.nonblocking()

  UnixPort = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  UnixPort.bind("/tmp/arduino.socket")
  UnixPort.listen(1)
  UnixPort.setblocking(0)

  while True:
    conn, addr = UnixPort.accept()
    Data = conn.recv(1024)
    if Data: 
      SerialPort.write(Data)
      conn.close()
    if SerialPort.inWaiting():
      print SerialPort.readline()
    
except Exception, e:
  os.remove("/tmp/arduino.socket")
  print(e)
  raise
