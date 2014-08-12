#!/usr/bin/python
import MySQLdb
import sys
import copy
import re
from email import *
from alarm import *
from sensor import *
from action import *

class DataBase:
  Req = {"Alarms" : "SELECT Actions.*, Alarms.* FROM Alarms, EventActions, Actions WHERE isactive=true AND Alarms.ID=EventActions.IDAlarm AND EventActions.IDAction=Actions.ID",
          "Emails" : "SELECT Actions.*, Emails.* FROM Emails, EventActions, Actions WHERE Emails.ID = EventActions.IDEmail AND EventActions.IDAction = Actions.ID",
          "Sensors": "SELECT Actions.*, Sensors.* FROM Sensors, EventActions, Actions WHERE Sensors.ID=EventActions.IDSensor AND EventActions.IDAction = Actions.ID"}
  Function = {"Alarms" : "self.GetAlarm",
              "Emails" : "self.GetEmail",
              "Sensors": "self.GetSensor"}
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
    self.DataBase.close()

  def GetAction(self, Row):
    if Row[2] != "": 
      Act = ArduinoAction(Row[2], Row[3])
    if Row[4] != "":
      Act = PushOverAction(Row[4], Row[5], Row[6])
    return Act

  def InitElements(self, List):
    CheckList = list()
    self.Cursor.execute(self.Req[List])
    LastID = 0
    Element = None
    for Row in self.Cursor.fetchall():
      if LastID != Row[7]:
        if Element != None:
          CheckList.append(Element)
        Element = eval(self.Function[List])(Row)
        LastID = Row[7]
      Element.AddAction(self.GetAction(Row)) 
    CheckList.append(Element)
    return CheckList

  def GetEmail(self, Row):
    if Row[12] == True:
      return ImapEmail(Row[8], Row[9], Row[10], Row[11], Row[12]) 
    else:
      return PopEmail(Row[8], Row[9], Row[10], Row[11], Row[12]) 

  def GetAlarm(self, Row):
    Date = list()
    for i in range(8, 13):
      Date.append(Row[i])
    WeekDays = list()
    for i in range(13, 20):
      WeekDays.append(Row[i])
    return Alarm(Date, WeekDays)

  def GetSensor(self, Row):
    return eval(Row[8])(Row[12], Row[13])
