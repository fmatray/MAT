#!/usr/bin/python
import serial
import logging
import socket
import os.path
from time import *
from sensor import *

class Arduino(object):
  _Instance = None
  Serial = True
  OutputData = ""
  InputData = ""

  def __new__(cls):
    if Arduino._Instance == None:
      Arduino._Instance = object.__new__(cls)
    return Arduino._Instance

  def __init__(self):
    try:
      if os.path.exists('/dev/ttyACM0'):
      	print "Connection on ttyACM0"
        self.Console = serial.Serial('/dev/ttyACM0', 9600) 
        self.Console.nonblocking()
      elif os.path.exists('/dev/ttyATH0'):
      	print "Connection on ttyATH0"
        self.Console = serial.Serial('/dev/ttyATH0', 9600) 
        self.Console.nonblocking()
      else:
      	print "Connecting on 127.0.0.1:6571"
        self.Serial = False
        self.Console = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Console.connect(('127.0.0.1', 6571))
    except Exception, e:
      raise

  def AddOutputData(self, Data):
    self.OutputData += Data

  def GetInputData(self):
    return self.InputData

  def Readable(self):
    return [self]

  def Writeable(self):
    if self.OutputData != "":
      return [self]
    return list()

  def Errored(self):
    return [self]

  def Send(self, Data = ""):
    Data = Data + self.OutputData
    self.OutputData = ""
    for D in Data.split('\n'):
      if D != "" and D[0] != '\r':
        logging.debug("Sending : " + D)
        if self.Serial == True:
          self.Console.write(D + '\n')
        else:
          self.Console.send(D + '\n')   
  def Readline(self):
    Data = ""
    if self.Serial == True:
      while (self.Console.inWaiting() > 0):
        Data += self.Console.readline(64)
    else:
      Data += self.Console.recv(64)
    logging.debug("Received :" + Data)
    self.InputData = Data
    return Data

  def Socket(self):
    return self.Console

  def fileno(self):
    return self.Console.fileno()

class ArduinoAction(Action):
  Arduino = None
  def __init__(self, Command, Argument= "", Arg3 = "", Arg4 = "", Arg5 = ""):
    if self.Arduino == None:
      self.Arduino = Arduino()
    self.Command = Command
    self.Argument = Argument

  def Action(self):
    self.Arduino.AddOutputData(str(self.Command) + ":" + str(self.Argument) + '\n')


class ArduinoSensor(Sensor):
  Arduino = None
  def __init__(self, Name, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    Sensor.__init__(self, Name, Threshold, MinMax, Argument3, Argument4)
    if ArduinoSensor.Arduino == None:
      ArduinoSensor.Arduino = Arduino()
    self.UpdateCommand = ""
 
  def Check(self):
    if self.Interval >= 0 and (datetime.datetime.now() - self.LastUpdateTime).seconds >= self.Interval and self.UpdateCommand != "":
      ArduinoSensor.AddOutputData(self.UpdateCommand + "\n")
    if self.ActionSent == True:
      return 

    if self.Analogic == False:
      if self.Value == self.Threshold:
        self.ActionSent = True
        ArduinoSensor.AddOutputData(self.Action())
    else:
      if self.MinMax == False and self.Value <= self.Threshold:
        self.ActionSent = True
        ArduinoSensor.AddOutputData(self.Action())
      if self.MinMax == True and self.Value >= self.Threshold:
        self.ActionSent = True
        ArduinoSensor.AddOutputData(self.Action())
    
class TemperatureSensor(ArduinoSensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    ArduinoSensor.__init__(self, "temperature", Threshold, MinMax)
    self.UpdateCommand = "temperaturesensor"

class LightSensor(ArduinoSensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    ArduinoSensor.__init__(self, "light", Threshold, MinMax)
    self.UpdateCommand = "lightsensor"

class SoundSensor(ArduinoSensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    ArduinoSensor.__init__(self, "sound", Threshold, MinMax)
    self.UpdateCommand = "soundsensor"

class LongButtonSensor(ArduinoSensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    ArduinoSensor.__init__(self, "longbutton", Threshold, MinMax)
    self.Interval = 0

class ShortButtonSensor(ArduinoSensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    ArduinoSensor.__init__(self, "shortbutton", Threshold, MinMax)
    self.Interval = 0
