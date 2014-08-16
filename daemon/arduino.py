#!/usr/bin/python
import serial
from time import *
from sensor import *

class Arduino(object):
  _Instance = None
  OutputData = ""
  InputData = ""

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
        print "Sending : " + D
        self.Console.write(D + '\n')
        
  def Readline(self):
    Data = ""
    while (self.Console.inWaiting() > 0):
      Data += self.Console.readline(1024)
      print "Received :" + Data
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

class TemperatureSensor(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "temperature", Threshold, MinMax)
    self.UpdateCommand = "temperaturesensor"

class LightSensor(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "light", Threshold, MinMax)
    self.UpdateCommand = "lightsensor"

class SoundSensor(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "sound", Threshold, MinMax)
    self.UpdateCommand = "soundsensor"

class LongButtonSensor(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "longbutton", Threshold, MinMax)
    self.Interval = 0

class ShortButtonSensor(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "shortbutton", Threshold, MinMax)
    self.Interval = 0
