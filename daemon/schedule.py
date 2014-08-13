#!/usr/bin/python
import time
import datetime
import sys
import copy
import re
from email import *
from alarm import *
from sensor import *

class Schedule:
  def __init__(self, DataBase):
    try:
      self.CheckList = []
      self.LocalTime = datetime.datetime.now()
      self.LastCheck = self.LocalTime
      self.CheckList = DataBase.InitElements()
      self.ParseLine = re.compile("\r\n")
      self.ParseElement = re.compile(":")
      self.ArduinoData = ""
    except Exception, e:
      print e
      raise
  
  def CheckStatus(self):
    for Element in self.CheckList:
      print Element
      self.ArduinoData += Element.Check()
  
  def UpdateSensor(self, ArduinoData):
    if ArduinoData == "":
      return
    for Line in self.ParseLine.split(ArduinoData):
      ParseList = self.ParseElement.split(Line)
      for Element in self.CheckList:
        if Element.IsSensor() == False:
          continue
        if ParseList[0] == Element.GetSensorName(): 
          self.ArduinoData += Element.Update(float(ParseList[1]))
        elif ParseList[0] == "button":
          if Element.GetSensorName() == "shortbutton":  
            self.ArduinoData += Element.Update(float(ParseList[1]))
          elif Element.GetSensorName() == "longbutton":  
            self.ArduinoData += Element.Update(float(ParseList[2]))

  def GetArduinoData(self):
    return self.ArduinoData

  def ResetArduinoData(self):
    self.ArduinoData = ""

  def Schedule(self):
    self.LocalTime = datetime.datetime.now()
    if self.LocalTime.second <= 10 and (self.LocalTime - self.LastCheck).seconds > 10:
      self.CheckStatus()
      self.LastCheck = self.LocalTime

