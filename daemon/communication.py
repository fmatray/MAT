#!/usr/bin/python
import socket
import sys
import os
import select

class Communication:
  def __init__(self):
    self.OpenSerialPort()
    self.OpenUnixSock()
    self.SerialData = ""
    self.UnixData = ""
    self.ClientSocket = None
    self.ReadList =  [self.UnixSock, self.SerialPort]
    self.WriteList = []
    self.ErrorList = [self.UnixSock, self.SerialPort]
  
  def AppendUnixData(self, s):
    self.UnixData += s
    self.WriteList.append(self.SerialPort)
  def AppendSerialData(self, s):
    self.SerialData += s
    self.WriteList.append(self.UnixSock)
  # Open Serial Port
  def OpenSerialPort(self):
    try:
      self.SerialPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      Self.SerialPort.connect("127.0.0.1", 6571)
    except Exception, e:
      print(e)
      raise
  def OpenUnixSock(self):
   # Make sure the socket does not already exist
   ServerAddress = './uds_socket'
   try:
     os.unlink(ServerAddress)
   except OSError:
     if os.path.exists(ServerAddress):
       raise
   # Create a UDS socket
   self.UnixSock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   # Bind the socket to the port
   print >>sys.stderr, 'starting up on %s' % ServerAddress
   self.UnixSock.bind(ServerAddress)
   # Listen for incoming connections
   self.UnixSock.listen(1)

  def ProcessReadable(self):
    for Socket in self.Readable:
      if Socket is self.UnixSock:
        #New Connection
        self.ClientSocket, ClientAddress = self.UnixSock.accept()
        self.ReadList.append(self.ClientSocket)
        self.ErrorList.append(self.ClientSocket)
        print "Connection from", ClientAddress
      elif Socket is self.SerialPort:
        self.SerialData += self.SerialPort.recv(1024)
          
        if self.ClientSocket == None:
          self.SerialData = ""
        else:
          self.WriteList.append(self.ClientSocket)
      else:
        self.UnixData += Socket.recv(1024)
        if self.UnixData == "kill\n":
          print "I DIED"
          sys.exit()
        if not self.UnixData:
          Socket.close()
          self.ReadList.remove(Socket)
          self.ErrorList.remove(Socket)
          self.ClientSocket = None
        else:
          self.WriteList.append(self.SerialPort)

  def ProcessWritable(self):
    for Socket in self.Writable:
      self.WriteList.remove(Socket)
      if Socket is self.SerialPort:
        Socket.send(self.UnixData)
        self.UnixData = ""
      else:
        Socket.send(self.SerialData)
        self.SerialData = ""

  def ProcessErrored(self):
    for Socket in self.Errored:
      if Socket is self.UnixSock or Socket is self.SerialPort:
        raise Exception() 
      else:
        Socket.close()
        self.ReadList.remove(Socket)
        self.ErrorList.remove(Socket)
  
  def CheckCommunication(self):
    try:
      self.Readable, self.Writable, self.Errored = select.select(self.ReadList, self.WriteList, self.ErrorList, 10)
      self.ProcessReadable()
      SerialData = self.SerialData
      UnixData = self.UnixData
      self.ProcessWritable()
      self.ProcessErrored()
      return (SerialData, UnixData)
    except Exception, e:
      print e
      raise
