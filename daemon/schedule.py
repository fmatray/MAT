#!/usr/bin/python
import time
import datetime
import MySQLdb
import sys
from threading import Timer

class Schedule:
  SerialData = ""
  def __init__(self, DataBase):
    try:
      self.Cursor = DataBase.cursor()
      self.Schedule()
    except Exception, e:
      print e
      DataBase.close()
      sys.exit()

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
  
  def GetSerialData(self):
    return self.SerialData

  def ResetSerialData(self):
    self.SerialData = ""

  def Schedule(self):
    self.Alarms()
    t = Timer(10, self.Schedule)
    t.start()

