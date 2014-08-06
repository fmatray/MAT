#!/usr/bin/python
import time
import MySQLdb
import sys
from threading import Timer
from time import sleep

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
    self.Cursor.execute("SELECT * FROM alarm WHERE isactive=true")
    R = ["0000","00","00","00","00"]
    for Row in self.Cursor.fetchall() :
      for i in range(0, 4):
        if Row[i + 1] == "*":
          R[i] = str(time.localtime()[i])
        else:
         R[i] = str(Row[i + 1])
      AlarmList.append(time.strptime(R[0] + "." + R[1] + "." + R[2] + " " + R[3] + ":" + R[4], "%Y.%m.%d %H:%M")) 
    return AlarmList
  
  def GetSerialData(self):
    return self.SerialData

  def ResetSerialData(self):
    self.SerialData = ""

  def Schedule(self):
    print "toto"
    AlarmList = self.GetAlarms()
    LocalTime = time.localtime()
    for Alarm in AlarmList:
      if Alarm < LocalTime:
        print "ALARM"
        self.SerialData = "alarm\n"
        AlarmList.remove(Alarm)
    t = Timer(2, self.Schedule)
    t.start()

