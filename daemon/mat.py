#!/usr/bin/python
import sys
import os
import traceback
import config 
import logging
from communication import *
from schedule import *
from database import *

# MAIN LOOP
try :
  # Log to file
  logging.basicConfig(
#    filename='daemon.log',
    level=logging.INFO,
    format='%(asctime)-15s %(levelname)s:%(filename)s:%(lineno)d -- %(message)s')   

# Log to console
  Console = logging.StreamHandler()
  Console.setLevel(logging.DEBUG)
  Console.setFormatter(logging.Formatter('%(levelname)s:%(filename)s:%(lineno)d -- %(message)s'))
  logging.getLogger().addHandler(Console)

# Log to syslog
  from logging.handlers import SysLogHandler
  Syslog = SysLogHandler(address='/dev/log')
  Syslog.setLevel(logging.INFO)
  Syslog.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)s:%(filename)s:%(lineno)d -- %(message)s'))
  logging.getLogger().addHandler(Syslog)

  logging.info("Starting Daemon")
  DataBase = DataBase()
  Config = DataBase.InitConfig()
  Sch = Schedule(DataBase)
  Com = Communication()


  while True:
   Sch.Schedule()
   Com.CheckCommunication()

except Exception, e:
  exc_type, exc_value, exc_traceback = sys.exc_info()
  logging.critical(traceback.format_exc()) 
