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
  SerialData = ""
  CheckList = []
  def __init__(self, DataBase):
    try:
      self.LocalTime = datetime.datetime.now()
      self.LastCheck = self.LocalTime
      self.Cursor = DataBase.cursor()
    #  self.InitEmailList()
    #  self.InitAlarmList()
      self.Temperature = Temperature("", "")
      self.Light = Light("", "")
      self.Sound = Sound("", "")
      self.LongButton = LongButton("", "")
      self.ShortButton = ShortButton("", "")
      self.CheckList.append(self.Temperature)
      self.CheckList.append(self.Light)
      self.CheckList.append(self.Sound)
      self.CheckList.append(self.LongButton)
      self.CheckList.append(self.ShortButton)
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
  
  def CheckStatus(self):
    for Element in self.CheckList:
      self.SerialData += Element.Check()
  
  def UpdateSensor(self, SerialData):
    if SerialData == "":
      return
    for Line in self.ParseLine.split(SerialData):
      ParseList = self.ParseElement.split(Line)
      if ParseList[0] == "temperature": 
        self.Temperature.Update(float(ParseList[1]))
      elif ParseList[0] == "light":
        self.Light.Update(float(ParseList[1]))
      elif ParseList[0] == "sound":
        self.Sound.Update(float(ParseList[1]))
      elif ParseList[0] == "button":
        self.ShortButton.Update(float(ParseList[1]))
        self.LongButton.Update(float(ParseList[2]))

  def GetSerialData(self):
    return self.SerialData

  def ResetSerialData(self):
    self.SerialData = ""

  def Schedule(self):
    self.LocalTime = datetime.datetime.now()
    if self.LocalTime.second <= 10 and (self.LocalTime - self.LastCheck).seconds > 10:
      self.CheckStatus()
      self.LastCheck = self.LocalTime

