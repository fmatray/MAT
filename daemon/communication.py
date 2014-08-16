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
    ClientSocket = ClientUnixSocket()
    for Socket in self.Readable:
      Data = Socket.Readline()
      if Socket is self.Arduino:
        ClientSocket.AddOutputData(Data)
      elif Socket is ClientSocket:
        self.Arduino.AddOutputData(Data)
        
  def ProcessWritable(self):
    for Socket in self.Writable:
      Socket.Send()

  def ProcessErrored(self):
    for Socket in self.Errored:
      print "Error"

  def CheckCommunication(self):
    try:
      self.ReadList = self.Arduino.Readable() + self.UnixSocket.Readable()
      self.WriteList = self.Arduino.Writeable() + self.UnixSocket.Writeable()
      print "----------------------------------------------"
      print self.ReadList
      print self.ReadList
      print "Select"
      self.Readable, self.Writable, self.Errored = select.select(self.ReadList, self.WriteList, self.ErrorList, 10)
      print self.Readable
      print self.Writable
      print self.Errored
      self.ProcessReadable()
      self.ProcessWritable()
      self.ProcessErrored()
    except Exception, e:
      print e
      raise
