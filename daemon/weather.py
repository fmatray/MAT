#!/usr/bin/python
import pyowm


class Weather(Sensor):
  def __init__(self):
    self.forecast = owm.three_hours_forecast("Lyon,fr")
    return

  def Update(self, Value = ""):
    return ""

  def Check(self):
    return ""
