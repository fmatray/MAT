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
    return self.Console.write(Data)

  def Readline(self):
    return self.Console.readline()

  def Socket(self):
    return self.Console
    
