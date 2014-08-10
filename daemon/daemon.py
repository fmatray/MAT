#!/usr/bin/python
import sys
import os
import traceback
from communication import *
from schedule import *
from database import *

# MAIN LOOP
try :
  DataBase = DataBase()
  Sch = Schedule(DataBase)
  Com = Communication()

  while True:
   Sch.Schedule()
   s = Sch.GetArduinoData()
   if s <> "":
     Com.AppendUnixData(s)
     Sch.ResetArduinoData()
   (ArduinoData, UnixData) = Com.CheckCommunication()
   Sch.UpdateSensor(ArduinoData)

except Exception, e:
  exc_type, exc_value, exc_traceback = sys.exc_info()
  print "*** print_tb:"
  traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
  print "*** print_exception:"
  traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
  print "*** print_exc:"
  traceback.print_exc()
  print "*** format_exc, first and last line:"
  formatted_lines = traceback.format_exc().splitlines()
  print formatted_lines[0]
  print formatted_lines[-1]
  print "*** format_exception:"
  print repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
  print "*** extract_tb:"
  print repr(traceback.extract_tb(exc_traceback))
  print "*** format_tb:"
  print repr(traceback.format_tb(exc_traceback))
  print "*** tb_lineno:", exc_traceback.tb_lineno
  DataBase.close()
  sys.exit()
