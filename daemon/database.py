#!/usr/bin/python
import MySQLdb
import sys
import copy
import re
import logging
from config import *
from email import *
from alarm import *
from sensor import *
from action import *


class DataBase:
  Req = {"Sensors": "SELECT Actions.*, Sensors.* FROM Sensors, EventActions, Actions WHERE Sensors.ID=EventActions.IDSensor AND EventActions.IDAction = Actions.ID"}
  Function = {"Sensors": "self.GetSensor"}
  def __init__(self):
    try:
      self.DataBase = MySQLdb.connect(read_default_file = "~/my.cnf") # name of the conf file
      self.DataBase.autocommit(True)
      self.Cursor = self.DataBase.cursor()
    except Exception, e:
      raise

  def Close(self):
    self.DataBase.close()

  def GetAction(self, Row):
    try:
      return eval(str(Row[2]) + "Action")(Row[4], Row[5], Row[6], Row[7], Row[8])
    except:
      return None

  def InitElements(self):
    CheckList = list()
    for Key in self.Req.keys():
      self.Cursor.execute(self.Req[Key])
      LastID = 0
      Element = None
      for Row in self.Cursor.fetchall():
        if LastID != Row[9]:
          LastID = Row[9]
          if Element != None:
            CheckList.append(Element)
          Element = eval(self.Function[Key])(Row)
        if Element != None:  
          Act = self.GetAction(Row)
          if (Act != None):
            Element.AddAction(Act)
      if Element != None:
        CheckList.append(Element)
    logging.info(CheckList)
    for i in CheckList:
      logging.info(i)
      logging.info(i.ActionList)
    return CheckList

  def GetEmail(self, Row):
    if Row[14] == True:
      return ImapEmail(Row[10], Row[11], Row[12], Row[13], Row[14]) 
    else:
      return PopEmail(Row[10], Row[11], Row[12], Row[13], Row[14]) 

  def GetAlarm(self, Row):
    Date = list()
    for i in range(10, 15):
      Date.append(Row[i])
    WeekDays = list()
    for i in range(15, 22):
      WeekDays.append(Row[i])
    return Alarm(Date, WeekDays)

  def GetSensor(self, Row):
    try:
      return eval(str(Row[10]) + "Sensor")(Row[11], Row[12], Row[13], Row[14])
    except:
      return None

  def InitConfig(self):
    self.Cursor.execute("SELECT * FROM `Config`")
    Config = Configuration()
    for Row in self.Cursor.fetchall():
      Config.AddKey(Row[1], Row[2], Row[3])
    return Config
