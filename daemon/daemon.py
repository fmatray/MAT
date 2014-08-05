#!/usr/bin/python
import select
import socket
import sys
import os
import serial

# Open Serial Port
def OpenSerialPort():
  try:
    return serial.Serial('/dev/ttyACM0', 9600)
  except Exception, e:
    print(e)
    sys.exit()

def OpenUnixSock():
  # Make sure the socket does not already exist
  ServerAddress = './uds_socket'
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
  return UnixSock

# Create lists for select
SerialPort = OpenSerialPort()
UnixSock = OpenUnixSock()
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
#New Connection
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
