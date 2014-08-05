#!/usr/bin/python
import time
import MySQLdb
from threading import Timer
from time import sleep

SerialData = ""
try:
  DataBase = MySQLdb.connect(host="localhost", # your host, usually localhost
    user="arduino", # your username
    passwd="toto", # your password
    db="arduino") # name of the data base
  Cursor = DataBase.cursor()
except Exception, e:
  print e
  DataBase.close()
  sys.exit()

def GetAlarms():
  AlarmList = []
  Cursor.execute("SELECT * FROM alarm WHERE isactive=true")
  R = ["0000","00","00","00","00"]
  for Row in Cursor.fetchall() :
    for i in range(0, 4):
      if Row[i + 1] == "*":
        R[i] = str(time.localtime()[i])
      else:
        R[i] = str(Row[i + 1])
    AlarmList.append(time.strptime(R[0] + "." + R[1] + "." + R[2] + " " + R[3] + ":" + R[4], "%Y.%m.%d %H:%M")) 
  return AlarmList
  
def GetSerialData():
  return SerialData

def ResetSerialData():
  global SerialData
  SerialData = ""

def Schedule():
  global SerialData
  AlarmList = GetAlarms()
  LocalTime = time.localtime()
  for Alarm in AlarmList:
    if Alarm < LocalTime:
      print "ALARM"
      SerialData = "alarm\n"
      AlarmList.remove(Alarm)
  t = Timer(2, Schedule)
  t.start()

