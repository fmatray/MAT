#!/usr/bin/python
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
