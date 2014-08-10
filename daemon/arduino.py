#!/usr/bin/python
import serial

class Arduino:
  def __init__(self):
    try:
      self.Console = serial.Serial('/dev/ttyACM0', 9600) 
    except Exception, e:
      print(e)
      raise
  def Send(self, Data):
    if Data == "":
       return ""
    for D in Data.split("\n"):
      self.Console.write(D + "\n")

  def Readline(self):
    Data = self.Console.readline()
    print "Received :" + Data
    return Data

  def Socket(self):
    return self.Console
    
