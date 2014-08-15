#!/usr/bin/python
import time
import datetime
import sys
import copy
import re
from email import *
from alarm import *
from sensor import *
from weather import *
from action import *

class Schedule:
  def __init__(self, DataBase):
    try:
      self.CheckList = []
      self.LocalTime = datetime.datetime.now()
      self.LastCheck = self.LocalTime
      self.CheckList = DataBase.InitElements()
      self.ParseLine = re.compile("\r\n")
      self.ParseElement = re.compile(":")
    except Exception, e:
      print e
      raise
  
  def Check(self):
    for Element in self.CheckList:
      Element.Check()
  
  def UpdateSensor(self, ArduinoData):
    if ArduinoData == "":
      return
    for Line in self.ParseLine.split(ArduinoData):
      ParseList = self.ParseElement.split(Line)
      for Element in self.CheckList:
        if Element.IsSensor() == False:
          continue
        if ParseList[0] == Element.GetSensorName(): 
          Element.Update(float(ParseList[1]))
        elif ParseList[0] == "button":
          if Element.GetSensorName() == "shortbutton":  
            Element.Update(float(ParseList[1]))
          elif Element.GetSensorName() == "longbutton":  
            Element.Update(float(ParseList[2]))

  def Schedule(self):
    self.LocalTime = datetime.datetime.now()
    if self.LocalTime.second <= 10 and (self.LocalTime - self.LastCheck).seconds > 10:
      self.Check()
      self.LastCheck = self.LocalTime

