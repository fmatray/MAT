#!/usr/bin/python
import serial
from time import *
class Arduino(object):
  _Instance = None
  OutputData = ""

  def __new__(cls):
    if Arduino._Instance == None:
      Arduino._Instance = object.__new__(cls)
    return Arduino._Instance

  def __init__(self):
    try:
      self.Console = serial.Serial('/dev/ttyACM0', 9600) 
      self.Console.nonblocking()
    except Exception, e:
      print(e)
      raise
  def AddOutputData(self, Data):
    self.OutputData += Data

  def IsWriteable(self):
    if self.OutputData != "":
      return True
    return False

  def Send(self, Data):
    Data = Data + self.OutputData
    self.OutputData = ""
    for D in Data.split('\n'):
      if D != "" and D[0] != '\r':
        print "Sending : " + D
        self.Console.write(D + '\n')
        
  def Readline(self):
    Data = ""
    while (self.Console.inWaiting() > 0):
      Data += self.Console.readline(1024)
      print "Received :" + Data
    return Data

  def Socket(self):
    return self.Console
    
