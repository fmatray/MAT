#!/usr/bin/python
import serial
from time import *
class Arduino:
  def __init__(self):
    try:
      self.Console = serial.Serial('/dev/ttyACM0', 9600) 
      self.Console.nonblocking()
    except Exception, e:
      print(e)
      raise
  def Send(self, Data):
    if Data == "":
       return ""
    for D in Data.split('\n'):
      if D != "" and D[0] != '\r':
        print "Sending : " + D
        print self.Console.write(D + '\n')
        
  def Readline(self):
    Data = ""
    while (self.Console.inWaiting() > 0):
      Data += self.Console.readline(1024)
      print "Received :" + Data
    return Data

  def Socket(self):
    return self.Console
    
