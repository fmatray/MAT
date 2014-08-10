#!/usr/bin/python
import MySQLdb
import sys
import copy
import re
from email import *
from alarm import *
from sensor import *

class DataBase:
  def __init__(self):
    try:
      self.DataBase = MySQLdb.connect(host="localhost", # your host, usually localhost
        user="arduino", # your username
        passwd="toto", # your password
        db="arduino") # name of the data base
      self.DataBase.autocommit(True)
      self.Cursor = self.DataBase.cursor()
    except Exception, e:
      print e
      raise
  def Close(self):
    self.DataBase.cole()

  def InitEmailList(self):
    CheckList = list()
    self.Cursor.execute("SELECT Emails . * , Actions . * FROM Emails, EventActions, Actions WHERE Emails.ID = EventActions.IDEmail AND EventActions.IDAction = Actions.ID")
    for Row in self.Cursor.fetchall():
      if Row[5] == True:
        E = ImapEmail(Row[1], Row[2], Row[3], Row[4], Row[5], Row[9], Row[10]) 
      else:
        E = PopEmail(Row[1], Row[2], Row[3], Row[4], Row[5], Row[9], Row[10]) 
      CheckList.append(E)
    return CheckList

  def InitAlarmList(self):
    CheckList = list()
    self.Cursor.execute("SELECT Alarms.*, Actions.* FROM Alarms, EventActions, Actions WHERE isactive=true AND Alarms.ID=EventActions.IDAlarm AND EventActions.IDAction=Actions.ID")
    LastID = 0
    A = None
    for Row in self.Cursor.fetchall():
      Date = list()
      for i in range(1, 6):
        Date.append(Row[i])
      WeekDays = list()
      for i in range(6, 13):
        WeekDays.append(Row[i])
      if LastID != Row[0]:
        if A != None:
          CheckList.append(A)
        A = Alarm(Date, WeekDays, Row[16], Row[17])
        LastID = Row[0]
      else:
        A.AddAction(Row[16], Row[17])
    CheckList.append(A)
    return CheckList

  def InitSensorList(self):
    CheckList = list()
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
        CheckList.append(S)
    return CheckList
