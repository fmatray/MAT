#!/usr/bin/python
import sys
import time
from daemon import Daemon
import os
import traceback
import argparse
import logging
from communication import *
from schedule import *
from database import *

DaemonActionHelp = """
    Start = Starts the daemon (default)
    Stop = Stops the daemon
    Restart = Restarts the daemon
    """
Parser = argparse.ArgumentParser(description='MAT : Maison AuTomatique')
Parser.add_argument("-D", "--daemon", help=DaemonActionHelp, action="store", dest="Daemon", choices=("start", "stop", "restart"), default=None)
Parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true", dest="Verbose", default=False)
Parser.add_argument("-d", "--debug", help="Debug mode", action="store_true", dest="Debug", default=False)
Args = Parser.parse_args()
print Args
try :
  Level = logging.ERROR
  if Args.Verbose:
    Level = logging.INFO
  if Args.Debug:
    Level = logging.DEBUG
    
  # Init Log
  logging.basicConfig(level=Level, format='%(asctime)-15s %(levelname)s:%(filename)s:%(lineno)d -- %(message)s')   
  
  if not Args.Daemon:
    # Log to console
    Console = logging.StreamHandler()
    Console.setLevel(Level)
    Console.setFormatter(logging.Formatter('%(levelname)s:%(filename)s:%(lineno)d -- %(message)s'))
    logging.getLogger().addHandler(Console)
  else:
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

except Exception, e:
  logging.critical("Setup Error")
  exc_type, exc_value, exc_traceback = sys.exc_info()
  logging.critical(traceback.format_exc())   
  sys.exit(1)
  
class MatDaemon(Daemon):
    def run(self):
      MainLoop()
      
# MAIN LOOP
def MainLoop():
  logging.info("Starting Mat")
  while True:
    try:
      Sch.Schedule()
      Com.CheckCommunication()
    except Exception, e:
      logging.critical("Main Loop Error")
      exc_type, exc_value, exc_traceback = sys.exc_info()
      logging.critical(traceback.format_exc())
      sys.exit(1)

if __name__ == "__main__":
  if Args.Daemon != None:
    Mat = MatDaemon("/var/run/mat.pid")
    if Args.Daemon == "start":
      Mat.start()
    elif Args.Daemon == "start":
      Mat.stop()
    elif Args.Daemon == "start":
      Mat.restart()
    else:
      logging.critical("Unknow option for daemon")
      sys.exit(1)
  else:
    MainLoop()
    
sys.exit(0)
    
    
    
