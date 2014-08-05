#!/usr/bin/python
import select
import socket
import sys
import os
import serial
from com import *
from threading import Timer
from time import sleep

def Alarm():
  print "Alarm"
  t = Timer(2, Alarm) 
  t.start()

# Create lists for select
SerialPort = OpenSerialPort()
UnixSock = OpenUnixSock()
ReadList =  [UnixSock, SerialPort]
WriteList = []
ErrorList = [UnixSock, SerialPort]
SerialData = ""
UnixData = ""
ClientSocket = None

def ProcessReadable():
  global SerialData
  global UnixData
  global ClientSocket
  for Socket in Readable:
    if Socket is UnixSock:
#New Connection
      ClientSocket, ClientAddress = UnixSock.accept()
      ReadList.append(ClientSocket)
      ErrorList.append(ClientSocket)
      print "Connection from", ClientAddress
    elif Socket is SerialPort:
      while SerialPort.inWaiting() > 0:
        SerialData += SerialPort.readline()
      WriteList.append(ClientSocket)
    else:
      global UnixData
      UnixData += Socket.recv(1024)
      if not UnixData:
        Socket.close()
        ReadList.remove(Socket)
        ErrorList.remove(Socket)
        ClientSocket = None
      else:
        WriteList.append(SerialPort)

def ProcessWritable():  
  global SerialData
  global UnixData
  for Socket in Writable:
   WriteList.remove(Socket)
   if Socket is SerialPort:
    Socket.write(UnixData)
    UnixData = ""
   else:
    Socket.send(SerialData)
    SerialData = ""

def ProcessErrored():
  for Socket in Errored:
    if Socket is UnixSock or Socket is SerialPort:
      sys.exit()
    else:
      Socket.close()
      ReadList.remove(Socket)
      ErrorList.remove(Socket)

# MAIN LOOP
t = Timer(2, Alarm) 
t.start()
while True:
  Readable, Writable, Errored = select.select(ReadList, WriteList, ErrorList)
  ProcessReadable()
  ProcessWritable()
  ProcessErrored()
