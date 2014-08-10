#!/usr/bin/python
import time
import datetime
import MySQLdb
import sys
import copy
import re
from email import *
from alarm import *
from sensor import *

class Schedule:
  ArduinoData = ""
  CheckList = []
  def __init__(self, DataBase):
    try:
      self.LocalTime = datetime.datetime.now()
      self.LastCheck = self.LocalTime
      self.Cursor = DataBase.cursor()
    #  self.InitEmailList()
    #  self.InitAlarmList()
      self.InitSensorList()
      self.ParseLine = re.compile("\r\n")
      self.ParseElement = re.compile(":")
    except Exception, e:
      print e
      raise
       
  def InitEmailList(self):
    self.Cursor.execute("SELECT Emails . * , Actions . * FROM Emails, EventActions, Actions WHERE Emails.ID = EventActions.IDEmail AND EventActions.IDAction = Actions.ID")
    for Row in self.Cursor.fetchall():
      if Row[5] == True:
        E = ImapEmail(Row[1], Row[2], Row[3], Row[4], Row[5], Row[9], Row[10]) 
      else:
        E = PopEmail(Row[1], Row[2], Row[3], Row[4], Row[5], Row[9], Row[10]) 
      self.CheckList.append(E)

  def InitAlarmList(self):
    self.Cursor.execute("SELECT Alarms.*, Actions.* FROM Alarms, EventActions, Actions WHERE isactive=true AND Alarms.ID=EventActions.IDAlarm AND EventActions.IDAction=Actions.ID")
    for Row in self.Cursor.fetchall():
      Date = list()
      for i in range(1, 6):
        Date.append(Row[i])
      WeekDays = list()
      for i in range(6, 13):
        WeekDays.append(Row[i])
      A = Alarm(Date, WeekDays, Row[16], Row[17])
      self.CheckList.append(A)

  def InitSensorList(self):
    self.Cursor.execute("SELECT Sensors.*, Actions.* FROM Sensors, EventActions, Actions WHERE Sensors.ID=EventActions.IDSensor AND EventActions.IDAction = Actions.ID")
    for Row in self.Cursor.fetchall():
      S = None
      if Row[1] == "Temperature":
        S  = Temperature(Row[5], Row[6], Row[9], Row[10])
      elif Row[1] == "Light":
        S = Light(Row[5], Row[6], Row[9], Row[10])
      elif Row[1] == "Sound":
        S = Sound(Row[5], Row[6], Row[9], Row[10])
      elif Row[1] == "LongButton":
        S = LongButton(Row[5], Row[6], Row[9], Row[10])
      elif Row[1] == "ShortButton":
        S = ShortButton(Row[5], Row[6], Row[9], Row[10])
      if S != None:
        self.CheckList.append(S)
    
  
  def CheckStatus(self):
    for Element in self.CheckList:
      self.ArduinoData += Element.Check()
  
  def UpdateSensor(self, ArduinoData):
    if ArduinoData == "":
      return
    for Line in self.ParseLine.split(ArduinoData):
      ParseList = self.ParseElement.split(Line)
      for Element in self.CheckList:
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

