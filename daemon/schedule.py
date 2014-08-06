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

  def GetAlarms(self):
    AlarmList = []
    IDList = []
    self.Cursor.execute("SELECT * FROM alarm WHERE isactive=true")
    R = ["0000","00","00","00","00"]
    for Row in self.Cursor.fetchall() :
      ID = Row[0]
      for i in range(0, 5):
        if Row[i + 1] == "*":
          ID = None
          R[i] = str(time.localtime()[i])
        else:
         R[i] = str(Row[i + 1])

      Alarm = datetime.datetime.strptime(R[0] + "." + R[1] + "." + R[2] + " " + R[3] + ":" + R[4], "%Y.%m.%d %H:%M")
      if Alarm >= datetime.datetime.now(): 
        AlarmList.append(Alarm) 
      elif ID <> None:
        IDList.append(Row[0])

    for ID in IDList:
      self.Cursor.execute("UPDATE alarm SET isactive=0 WHERE ID =" + str(ID))
    return AlarmList
  
  def GetSerialData(self):
    return self.SerialData

  def ResetSerialData(self):
    self.SerialData = ""

  def Schedule(self):
    AlarmList = self.GetAlarms()
    LocalTime = datetime.datetime.now()
    for Alarm in AlarmList:
      if Alarm < LocalTime and LocalTime < Alarm + datetime.timedelta(0, 10):
        print "ALARM"
        self.SerialData = "alarm\n"
        AlarmList.remove(Alarm)
    t = Timer(2, self.Schedule)
    t.start()

