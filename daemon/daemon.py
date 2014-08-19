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
    filename='daemon.log',
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
   Sch.UpdateSensor()

except Exception, e:
  exc_type, exc_value, exc_traceback = sys.exc_info()
  logging.critical("*** print_tb:")
  traceback.logging.critical(_tb(exc_traceback, limit=1, file=sys.stdout))
  logging.critical("*** print_exception:")
  traceback.logging.critical(_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout))
  logging.critical("*** print_exc:")
  traceback.logging.critical(_exc())
  logging.critical("*** format_exc, first and last line:")
  formatted_lines = traceback.format_exc().splitlines()
  logging.critical(formatted_lines[0])
  logging.critical(formatted_lines[-1])
  logging.critical("*** format_exception:")
  logging.critical(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
  logging.critical("*** extract_tb:")
  logging.critical(repr(traceback.extract_tb(exc_traceback)))
  logging.critical("*** format_tb:")
  logging.critical(repr(traceback.format_tb(exc_traceback)))
  logging.critical("*** tb_lineno:", exc_traceback.tb_lineno)
  DataBase.Close()
  sys.exit()
