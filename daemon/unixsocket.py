#!/usr/bin/python
import socket
import sys
import os
import logging

class ClientUnixSocket(object):
  _Instance = None
  ClientSocket = None
  OutputData = ""
  InputData = ""

  def __new__(cls, Socket = None):
    if ClientUnixSocket._Instance == None:
      ClientUnixSocket._Instance = object.__new__(cls)
    return ClientUnixSocket._Instance

  def __init__(self, Socket = None): 
    if Socket != None:
      self.ClientSocket, ClientAddress = Socket.accept()
      logging.info("New Client")

  def __del__(self):
    logginf.info("Closing client")
    self.ClientUnixSocket.close()

  def AddOutputData(self, Data):
    if self.ClientSocket != None:
      self.OutputData += Data
  def GetInputData(self):
    return self.InputData

  def Send(self, Data = ""):
    Data += self.OutputData
    self.OutputData = ""
    if self.ClientSocket != None:
      self.ClientSocket.send(Data)

  def Readline(self):
    self.InputData = ""
    if self.ClientSocket != None:  
      self.InputData = self.ClientSocket.recv(1024)
      if not self.InputData:
        self.ClientSocket.close()
        UnixSocket().ResetClientSocket()
        return ""
      if self.InputData == "kill\n":
        logging.info("This is the end")
        sys.exit()
      logging.debug(self.InputData)
    return self.InputData

  def Writeable(self):
    if self.ClientSocket != None and self.OutputData!= "":
      return [self]
    return []

  def fileno(self):
    return self.ClientSocket.fileno()

class UnixSocket(object):
  _Instance = None
  UnixSocket = None
  ClientSocket = None

  def __new__(cls):
    if UnixSocket._Instance == None:
      UnixSocket._Instance = object.__new__(cls)
    return UnixSocket._Instance

  def __init__(self):
    self.OpenUnixSock()

  def Readable(self):
    if self.ClientSocket != None:
      return[self.ClientSocket]
    return [self] 

  def Writeable(self):
    if self.ClientSocket != None:
      return self.ClientSocket.Writeable()
    return []

  def Errored(self):
    if self.ClientSocket != None:
      return [self, self.ClientSocket]
    return [self]

  def Send(self, Data= ""):
    return

  def Readline(self):
    self.ClientSocket = ClientUnixSocket(self.UnixSocket)
    return ""
     
  def fileno(self):
    return self.UnixSocket.fileno()

  def ResetClientSocket(self):
    try:
      del self.ClientSocket
      self.ClientSocket = None
    except:
      pass
    self.ClientSocket = None

  def OpenUnixSock(self):
   # Make sure the socket does not already exist
   ServerAddress = './uds_socket'
   try:
     os.unlink(ServerAddress)
   except OSError:
     if os.path.exists(ServerAddress):
       raise
   # Create a UDS socket
   self.UnixSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # Bind the socket to the port
   logging.info('starting up on %s' % ServerAddress)
#   self.UnixSocket.bind(ServerAddress)
   try:
    self.UnixSocket.bind(("127.0.0.1", "8888"))
   except socket.error as msg:
    loggin.critical('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
   # Listen for incoming connections
   self.UnixSocket.listen(1)

