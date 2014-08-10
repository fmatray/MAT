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
    print "Send : " + Data
    return self.Console.write(Data)

  def Readline(self):
    R = self.Console.readline()
    print "Reading : " + R
    return R

  def Socket(self):
    return self.Console
    
