#!/usr/bin/python
import time
import datetime
from basecheck import *

class Alarm(BaseCheck):
  def __init__(self, Date, WeekDays, Command = "", Argument = ""):
    try:
      BaseCheck.__init__(self, Command, Argument)
      self.Date = Date
      self.WeekDays = WeekDays
    except Exception, e:
      print e

  def Check(self):
# ALARM on date and time 
    print "CHECK ALARM"
    LocalTime = datetime.datetime.now()
    Date = list()
    i = 0
    for Element in self.Date:
      if Element == "*":
        Date.append(str(LocalTime.timetuple()[i]))
      else:
        Date.append(str(Element))
      i += 1

    CalculatedAlarm = datetime.datetime.strptime(Date[0] + "." + Date[1] + "." + Date[2] + " " + Date[3] + ":" + Date[4], "%Y.%m.%d %H:%M")
    if CalculatedAlarm < LocalTime and LocalTime < CalculatedAlarm + datetime.timedelta(0, 10):
      return self.Action()
# ALARM on week day
    for i in range(0, 6):
      if self.WeekDays[i] == 1 and i == time.localtime()[6] and CalculatedAlarm < LocalTime and LocalTime < CalculatedAlarm + datetime.timedelta(0, 10):
        return self.Action()
    return ""
