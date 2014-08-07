#!/usr/bin/python
import time
import datetime
import MySQLdb
import sys
import copy
from email import *
from alarm import *

class Schedule:
  SerialData = ""
  CheckList = []
  def __init__(self, DataBase):
    try:
      self.LocalTime = datetime.datetime.now()
      self.LastCheck = self.LocalTime
      self.Cursor = DataBase.cursor()
    #  self.InitEmailList()
      self.InitAlarmList()
      self.Schedule()
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
  
  def GetSerialData(self):
    return self.SerialData

  def ResetSerialData(self):
    self.SerialData = ""

  def Schedule(self):
    self.LocalTime = datetime.datetime.now()
    if self.LocalTime.second <= 10 and (self.LocalTime - self.LastCheck).seconds > 10:
      self.CheckStatus()
      self.LastCheck = self.LocalTime

