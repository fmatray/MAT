#!/usr/bin/python
import socket
import sys
import os
import select
from arduino import *
    
class Communication:
  def __init__(self):
    self.OpenUnixSock()
    self.ArduinoData = ""
    self.UnixData = ""
    self.ClientSocket = None
    self.Arduino = Arduino()
    self.ReadList =  [self.UnixSock, self.Arduino.Socket()]
    self.WriteList = []
    self.ErrorList = [self.UnixSock, self.Arduino.Socket()]
  
  def AppendUnixData(self, s):
    self.UnixData += s
    self.WriteList.append(self.Arduino.Socket())

  def AppendArduinoData(self, s):
    self.ArduinoData += s
    self.WriteList.append(self.UnixSock)
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
      elif Socket is self.Arduino.Socket():
        self.ArduinoData += self.Arduino.Readline()
        if self.ClientSocket == None:
          self.ArduinoData = ""
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
          self.WriteList.append(self.Arduino.Socket())

  def ProcessWritable(self):
    for Socket in self.Writable:
      self.WriteList.remove(Socket)
      if Socket is self.Arduino.Socket():
        self.Arduino.Send(self.UnixData)
        self.UnixData = ""
      else:
        Socket.send(self.ArduinoData)
        self.ArduinoData = ""

  def ProcessErrored(self):
    for Socket in self.Errored:
      if Socket is self.UnixSock or Socket is self.Arduino.Socket():
        raise Exception() 
      else:
        Socket.close()
        self.ReadList.remove(Socket)
        self.ErrorList.remove(Socket)
  
  def CheckCommunication(self):
    try:
      if self.Arduino.IsWriteable():
        self.WriteList.append(self.Arduino.Socket())
      self.Readable, self.Writable, self.Errored = select.select(self.ReadList, self.WriteList, self.ErrorList, 10)
      self.ProcessReadable()
      ArduinoData = self.ArduinoData
      UnixData = self.UnixData
      self.ProcessWritable()
      self.ProcessErrored()
      return (ArduinoData, UnixData)
    except Exception, e:
      print e
      raise
