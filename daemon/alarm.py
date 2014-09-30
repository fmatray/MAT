#!/usr/bin/python
import time
import datetime
from sensor import *

class AlarmSensor(Sensor):
  def __init__(self, Date, Hours, WeekDays, Argument3 = "", Argument4 = ""):
    Sensor.__init__(self)
    self.Date = Date.split("/") + Hours.split(":")
    self.WeekDays = WeekDays.split(":")

  def Update(self):
    return

  def Check(self):
# ALARM on date and time 
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
      self.Action()
      return
# ALARM on week day
    for i in range(0, 6):
      if self.WeekDays[i] == 1 and i == time.localtime()[6] and CalculatedAlarm < LocalTime and LocalTime < CalculatedAlarm + datetime.timedelta(0, 10):
        self.Action()
