#!/usr/bin/python
import datetime

class Sensor:
  def __init__(self, Name, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    self.ActionList = []
    self.Name = Name
    self.Threshold = Threshold
    self.MinMax = MinMax
    self.LastUpdateTime = datetime.datetime.now() 
    self.Value = 0.0
    self.ActionSent = False
    self.Analogic = True
    self.Interval = 120
    
  def GetSensorName(self):
    return self.Name
    
  def AddAction(self, Act):
    self.ActionList.append(Act)
  def Action(self):
    for Action in self.ActionList:
      Action.Action()

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


