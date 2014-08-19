#!/usr/bin/python
import socket
import sys
import os
import select
from arduino import *
from unixsocket import * 

class Communication:
  def __init__(self):
    self.Arduino = Arduino()
    self.UnixSocket = UnixSocket()
    self.ReadList =  []
    self.WriteList = []
    self.ErrorList = []

  def ProcessReadable(self):
    for Socket in self.Readable:
      Data = Socket.Readline()
      ClientSocket = ClientUnixSocket()
      if ClientSocket == None:
        return
      if Socket is self.Arduino:
        ClientSocket.AddOutputData(Data)
      elif Socket is ClientSocket:
        self.Arduino.AddOutputData(Data)
        
  def ProcessWritable(self):
    for Socket in self.Writable:
      Socket.Send()

  def ProcessErrored(self):
    ClientSocket = ClientUnixSocket()
    for Socket in self.Errored:
      if Socket is ClientSocket:
        self.UnixSocket.ResetClientSocket() 
      logging.error("Error with " + str(Socket))

  def CheckCommunication(self):
    try:
      self.ReadList = self.Arduino.Readable() + self.UnixSocket.Readable()
      self.WriteList = self.Arduino.Writeable() + self.UnixSocket.Writeable()
      self.Errored = self.Arduino.Errored() + self.UnixSocket.Errored()
      self.Readable, self.Writable, self.Errored = select.select(self.ReadList, self.WriteList, self.ErrorList, 10)
      if len(self.Errored) > 0: 
        self.ProcessErrored()
      else:
        self.ProcessReadable()
        self.ProcessWritable()
    except Exception, e:
      raise
