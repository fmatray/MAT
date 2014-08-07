#!/usr/bin/python
import time
import datetime
import MySQLdb
import sys
import copy
from email import *

class Schedule:
  SerialData = ""
  CheckList = []
  def __init__(self, DataBase):
    try:
      self.LocalTime = datetime.datetime.now()
      self.Cursor = DataBase.cursor()
      self.InitCheckList()
      self.Schedule()
    except Exception, e:
      print e
      raise
       
  def InitCheckList(self):
    self.Cursor.execute("SELECT Emails . * , Actions . * FROM Emails, EventActions, Actions WHERE Emails.ID = EventActions.IDEmail AND EventActions.IDAction = Actions.ID")
    for Row in self.Cursor.fetchall():
      if Row[5] == True:
        E = ImapEmail(Row[1], Row[2], Row[3], Row[4], Row[5], Row[9], Row[10]) 
      else:
        E = PopEmail(Row[1], Row[2], Row[3], Row[4], Row[5], Row[9], Row[10]) 
      self.CheckList.append(E)

  def Alarms(self):
    IDList = []
    self.Cursor.execute("SELECT Alarms.*, Actions.* FROM Alarms, EventActions, Actions WHERE isactive=true AND Alarms.ID=EventActions.IDAlarm AND EventActions.IDAction=Actions.ID")
    R = ["0000","00","00","00","00"]
    for Row in self.Cursor.fetchall():
     
      ID = Row[0]
      for i in range(0, 5):
        if Row[i + 1] == "*":
          ID = None
          R[i] = str(time.localtime()[i])
        else:
         R[i] = str(Row[i + 1])
# ALARM on date and time 
      Alarm = datetime.datetime.strptime(R[0] + "." + R[1] + "." + R[2] + " " + R[3] + ":" + R[4], "%Y.%m.%d %H:%M")
      if Alarm < self.LocalTime and self.LocalTime < Alarm + datetime.timedelta(0, 10):
        self.SerialData += Row[16] + ":"+ Row[17] +"\n"
# ALARM on week day
      for i in range(0, 6):
        if Row[i + 6] == 1:
          ID = None
          if i == time.localtime()[6] and Alarm < self.LocalTime and self.LocalTime < Alarm + datetime.timedelta(0, 10):
            self.SerialData += Row[16] + ":"+ Row[17] +"\n"
# REMOVE old alarm
      if ID <> None:
        IDList.append(Row[0])
    for ID in IDList:
      self.Cursor.execute("UPDATE alarm SET isactive=0 WHERE ID =" + str(ID))
  
  def CheckStatus(self):
    for E in self.CheckList:
      self.SerialData += E.Check()
  
  def GetSerialData(self):
    return self.SerialData

  def ResetSerialData(self):
    self.SerialData = ""

  def Schedule(self):
    self.LocalTime = datetime.datetime.now()
    #if self.LocalTime.second <= 10:
    self.Alarms()
    self.CheckStatus()

