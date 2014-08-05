#!/usr/bin/python
import select
import socket
import sys
import os
import serial

ServerAddress = './uds_socket'
# Open Serial
try:
  SerialPort = serial.Serial('/dev/ttyACM0', 9600)
#  SerialPort.nonblocking()
except Exception, e:
  print(e)
  sys.exit()

# Make sure the socket does not already exist
try:
  os.unlink(ServerAddress)
except OSError:
  if os.path.exists(ServerAddress):
    raise
# Create a UDS socket
UnixSock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# Bind the socket to the port
print >>sys.stderr, 'starting up on %s' % ServerAddress
UnixSock.bind(ServerAddress)

# Listen for incoming connections
UnixSock.listen(1)

ReadList =  [UnixSock, SerialPort]
WriteList = []
ErrorList = [UnixSock, SerialPort]
UnixData = ""
SerialData = ""
ClientSocket = None
while True:
  Readable, Writable, Errored = select.select(ReadList, WriteList, ErrorList)
  for Socket in Readable:
    if Socket is UnixSock:
      ClientSocket, ClientAddress = UnixSock.accept()
      ReadList.append(ClientSocket)
      print "Connection from", ClientAddress
    elif Socket is SerialPort:
      while SerialPort.inWaiting() > 0:
        SerialData += SerialPort.readline()
      WriteList.append(ClientSocket)
    else:
      UnixData += Socket.recv(1024)
      if not UnixData:
        Socket.close()
        ReadList.remove(Socket)
        ClientSocket = None
      else:
        WriteList.append(SerialPort)
  
  for Socket in Writable:
   WriteList.remove(Socket)
   if Socket is SerialPort:
    Socket.write(UnixData)
    UnixData = ""
   else:
    Socket.send(SerialData)
    SerialData = ""
