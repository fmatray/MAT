#!/usr/bin/python
from sensor import *
import pyowm
import config

class Weather(Sensor):
  Rain = False 
  Fog = False 
  Snow = False
  Clouds = False
  _Instance = None
 
  def __new__(Class):
    if Class._Instance == None:
      Class._Instance = Sensor
    return Class._Instance

  def __init__(self):
    self.City = config.Config.GetKey("Weather", "City") 
    self.Token = config.Config.GetKey("Weather", "Token") 
    self.owm = pyowm.OWM(self.Token)
    return

  def Update(self, Value = ""):
    return ""

  def Check(self):
    self.forecast = self.owm.three_hours_forecast(self.City)
    self.Rain = self.forecast.will_have_rain()
    self.Fog = self.forecast.will_have_fog()
    self.Snow = self.forecast.will_have_snow()
    self.Clouds = self.forecast.will_have_clouds()
    return ""

class Rain(Weather):
  def __init__(self):
   Weather.__init__(self)
   return
