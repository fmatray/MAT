#!/usr/bin/python
import sys
import os
import traceback
import argparse
import logging
from communication import *
from schedule import *
from database import *

Parser = argparse.ArgumentParser(description='MAT : Maison AuTomatique')
Parser.add_argument("--verbose", help="Increase output verbosity", action="store_true")
Parser.add_argument("--debug", help="Debug mode", action="store_true")
Parser.add_argument("--daemon", help="Daemonize MAT", action="store_true")

Args = Parser.parse_args()

try :
  Level = logging.ERROR
  if Arsg.verbose:
    Level = logging.INFO
  if Arsg.debug:
    Level = logging.DEBUG
    
  # Init Log
  logging.basicConfig(
    level=Level,
    format='%(asctime)-15s %(levelname)s:%(filename)s:%(lineno)d -- %(message)s')   

  if not Args.daemon:
    # Log to console
    Console = logging.StreamHandler()
    Console.setLevel(Level)
    Console.setFormatter(logging.Formatter('%(levelname)s:%(filename)s:%(lineno)d -- %(message)s'))
    logging.getLogger().addHandler(Console)
  else
    # Log to syslog
    from logging.handlers import SysLogHandler
    Syslog = SysLogHandler(address='/dev/log')
    Syslog.setLevel(Level)
    Syslog.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)s:%(filename)s:%(lineno)d -- %(message)s'))
    logging.getLogger().addHandler(Syslog)

  logging.info("Setting Mat")
  DataBase = DataBase()
  Config = DataBase.InitConfig()
  Sch = Schedule(DataBase)
  Com = Communication()

  logging.info("Starting Mat")
# MAIN LOOP TO DAEMONIZE
  while True:
   Sch.Schedule()
   Com.CheckCommunication()

except Exception, e:
  exc_type, exc_value, exc_traceback = sys.exc_info()
  logging.critical(traceback.format_exc()) 
