#!/usr/bin/python
import sys
import os
import MySQLdb
from communication import *
from schedule import *

# MAIN LOOP
try :
  DataBase = MySQLdb.connect(host="localhost", # your host, usually localhost
    user="arduino", # your username
    passwd="toto", # your password
    db="arduino") # name of the data base
  Sch = Schedule(DataBase)
  Com = Communication()

  while True:
   s = Sch.GetSerialData()
   if s <> "":
     Com.AppendUnixData(s)
     Sch.ResetSerialData()
   Com.CheckCommunication()
except Exception, e:
  print e
  DataBase.close()
  sys.exit()
