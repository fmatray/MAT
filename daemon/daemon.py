#!/usr/bin/python
import select
import socket
import sys
import os
import serial
import MySQLdb
from com import *
from schedule import *

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
      print SerialData
      if ClientSocket == None:
        SerialData = ""
      else:
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
try :
  DataBase = MySQLdb.connect(host="localhost", # your host, usually localhost
    user="arduino", # your username
    passwd="toto", # your password
    db="arduino") # name of the data base
  Sch = Schedule(DataBase)

  while True:
   s = Sch.GetSerialData()
   if s <> "":
     UnixData += s
     WriteList.append(SerialPort)
     Sch.ResetSerialData()
   Readable, Writable, Errored = select.select(ReadList, WriteList, ErrorList, 10)
   ProcessReadable()
   ProcessWritable()
   ProcessErrored()
except Exception, e:
  print e
  sys.exit()
