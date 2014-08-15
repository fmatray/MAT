#!/usr/bin/python
import datetime
from basecheck import *

class Sensor(BaseCheck):
  Arduino = None
  def __init__(self, Name, Threshold, MinMax):
    if self.Arduino == None:
      self.Arduino = Arduino()
    BaseCheck.__init__(self)
    self.Name = Name
    self.Threshold = Threshold
    self.MinMax = MinMax
    self.LastUpdateTime = datetime.datetime.now() 
    self.Value = 0.0 
    self.ActionSent = False
    self.Analogic = True
    self.Interval = 120
    self.UpdateCommand = ""

  def IsSensor(self):
    return True

  def Update(self, Value):
    self.Value = Value
    self.LastUpdateTime = datetime.datetime.now() 
    if self.ActionSent == True:
      if self.MinMax == False and self.Value >= self.Threshold:
        self.ActionSent = False
      if self.MinMax == True and self.Value <= self.Threshold:
        self.ActionSent = False
    return ""

  def Check(self):
    if self.Interval >= 0 and (datetime.datetime.now() - self.LastUpdateTime).seconds >= self.Interval and self.UpdateCommand != "":
      Arduino.AddOutputData(self.UpdateCommand + "\n")
    if self.ActionSent == True:
      return 

    if self.Analogic == False:
      if self.Value == self.Threshold:
        self.ActionSent = True
        Arduino.AddOutputData(self.Action())
    else:
      if self.MinMax == False and self.Value <= self.Threshold:
        self.ActionSent = True
        Arduino.AddOutputData(self.Action())
      if self.MinMax == True and self.Value >= self.Threshold:
        self.ActionSent = True
        Arduino.AddOutputData(self.Action())

  def GetSensorName(self):
    return self.Name

class Temperature(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "temperature", Threshold, MinMax)
    self.UpdateCommand = "temperaturesensor"

class Light(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "light", Threshold, MinMax)
    self.UpdateCommand = "lightsensor"

class Sound(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "sound", Threshold, MinMax)
    self.UpdateCommand = "soundsensor"

class LongButton(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "longbutton", Threshold, MinMax)
    self.Interval = 0

class ShortButton(Sensor):
  def __init__(self, Threshold, MinMax):
    Sensor.__init__(self, "shortbutton", Threshold, MinMax)
    self.Interval = 0
