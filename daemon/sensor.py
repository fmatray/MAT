#!/usr/bin/python
import datetime
from basecheck import *

class Sensor(BaseCheck):
  def __init__(self, Name, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    BaseCheck.__init__(self)
    self.Name = Name
    self.Threshold = Threshold
    self.MinMax = MinMax
    self.LastUpdateTime = datetime.datetime.now() 
    self.Value = 0.0
    self.ActionSent = False
    self.Analogic = True
    self.Interval = 120

  def IsSensor(self):
    return True

  def Update(self, Value = None):
    if Value != None:
      self.Value = Value
    self.LastUpdateTime = datetime.datetime.now() 
    if self.ActionSent == True:
      if self.MinMax == False and self.Value >= self.Threshold:
        self.ActionSent = False
      if self.MinMax == True and self.Value <= self.Threshold:
        self.ActionSent = False

  def Check(self):
    if self.Interval >= 0 and (datetime.datetime.now() - self.LastUpdateTime).seconds >= self.Interval and self.UpdateCommand != "":
      self.Update()
    if self.ActionSent == True:
      return 

    if self.Analogic == False:
      if self.Value == self.Threshold:
        self.ActionSent = True
        self.Action()
    else:
      if self.MinMax == False and self.Value <= self.Threshold:
        self.ActionSent = True
        self.Action()
      if self.MinMax == True and self.Value >= self.Threshold:
        self.ActionSent = True
        self.Action()

  def GetSensorName(self):
    return self.Name
