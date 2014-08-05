#!/usr/bin/python
from threading import Timer
from time import sleep

def Schedule():
  print "Alarm"
  t = Timer(2,Schedule)
  t.start()

