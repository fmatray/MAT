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
      self.Cursor = DataBase.cursor()
      self.Cursor.execute("SELECT * FROM emails")
      for Row in self.Cursor.fetchall():
        if Row[5] == True:
          E = ImapEmail(Row[1], Row[2], Row[3], Row[4], Row[5]) 
        else:
          E = PopEmail(Row[1], Row[2], Row[3], Row[4], Row[5]) 
        self.CheckList.append(E)
      self.Schedule()
    except Exception, e:
      print e
      raise
       
  def Alarms(self):
    IDList = []
    LocalTime = datetime.datetime.now()
    self.Cursor.execute("SELECT * FROM alarm WHERE isactive=true")
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
      if Alarm < LocalTime and LocalTime < Alarm + datetime.timedelta(0, 10):
        self.SerialData += "alarm\n"
# ALARM on week day
      for i in range(0, 6):
        if Row[i + 6] == 1:
          ID = None
          if i == time.localtime()[6] and Alarm < LocalTime and LocalTime < Alarm + datetime.timedelta(0, 10):
            self.SerialData += "alarm\n"
# REMOVE old alarm
      if ID <> None:
        IDList.append(Row[0])
    for ID in IDList:
      self.Cursor.execute("UPDATE alarm SET isactive=0 WHERE ID =" + str(ID))
  
  def CheckStatus(self):
    for E in self.CheckList:
      if E.Check() == True:
        self.SerialData += "notification:1\n"
  
  def GetSerialData(self):
    return self.SerialData

  def ResetSerialData(self):
    self.SerialData = ""

  def Schedule(self):
    self.CheckStatus()
    self.Alarms()

