#!/usr/bin/python
import datetime
from basecheck import *

class Sensor(BaseCheck):
  Value = 0.0 
  ActionSent = False
  Interval = 120
  UpdateCommand = ""
  def __init__(self, Name, Threshold, MinMax, Command, Argument):
    BaseCheck.__init__(self, Command, Argument)
    self.Name = Name
    self.Threshold = Threshold
    self.MinMax = MinMax
    self.LastUpdateTime = datetime.datetime.now() 

  def IsSensor(self):
    return True

  def Update(self, Value):
    self.Value = Value
    self.LastUpdateTime = datetime.datetime.now() 
    if self.ActionSent == True:
      if self.MinMax == False and self.Value > self.Threshold:
        self.ActionSent = False
      if self.MinMax == True and self.Value < self.Threshold:
        self.ActionSent = False
    return ""

  def Check(self):
    print self.Value
    Ret = ""
    if self.Interval > 0 and (datetime.datetime.now() - self.LastUpdateTime).seconds > self.Interval:
      Ret = self.UpdateCommand + "\n"
    if self.ActionSent == True:
      return Ret    
    if self.MinMax == False and self.Value < self.Threshold:
      self.ActionSent = True
      Ret += self.Action()
    if self.MinMax == True and self.Value > self.Threshold:
      self.ActionSent = True
      Ret += self.Action()
    return Ret

  def GetSensorName(self):
    return self.Name

class Temperature(Sensor):
  def __init__(self, Threshold, MinMax, Command, Argument):
    Sensor.__init__(self, "temperature", Threshold, MinMax, Command, Argument)
    self.UpdateCommand = "temperaturesensor"

class Light(Sensor):
  def __init__(self, Threshold, MinMax, Command, Argument):
    Sensor.__init__(self, "light", Threshold, MinMax, Command, Argument)
    self.UpdateCommand = "lightsensor"

class Sound(Sensor):
  def __init__(self, Threshold, MinMax, Command, Argument):
    Sensor.__init__(self, "sound", Threshold, MinMax, Command, Argument)
    self.UpdateCommand = "soundsensor"

class LongButton(Sensor):
  def __init__(self, Threshold, MinMax, Command, Argument):
    Sensor.__init__(self, "longbutton", Threshold, MinMax, Command, Argument)
    self.Interval = 0

class ShortButton(Sensor):
  def __init__(self, Threshold, MinMax, Command, Argument):
    Sensor.__init__(self, "shortbutton", Threshold, MinMax, Command, Argument)
    self.Interval = 0
