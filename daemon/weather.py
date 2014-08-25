#!/usr/bin/python
from sensor import *
import pyowm
import config
import datetime

class Weather(object):
  _Instance = None
 Configured = False
 
  def __new__(cls):
    if Weather._Instance == None:
      Weather._Instance = object.__new__(cls)
    return Weather._Instance

  def __init__(self):
    if self.Configured == True:
      return
    self.City = config.Config.GetKey("Weather", "City") 
    self.Token = config.Config.GetKey("Weather", "Token") 
    self.Owm = pyowm.OWM(self.Token)
    self.Rain = False 
    self.Fog = False 
    self.Snow = False
    self.Clouds = False
    self.LastUpdateTime = None 
    self.Update()
    self.Configured = True

  def Update(self):
    if self.LastUpdateTime == None or (datetime.datetime.now() - self.LastUpdateTime).seconds > 3600:
      self.LastUpdateTime = datetime.datetime.now()
      self.Forecast = self.Owm.three_hours_forecast(self.City)
      self.Rain = self.Forecast.will_have_rain()
      self.Fog = self.Forecast.will_have_fog()
      self.Snow = self.Forecast.will_have_snow()
      self.Clouds = self.Forecast.will_have_clouds()

  def GetRain(self):
    return self.Rain
  def GetFog(self):
    return self.Fog
  def GetSnow(self):
    return self.Snow
  def GetClouds(self):
    return self.Clouds

class RainSensor(Sensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    Sensor.__init__(self, "rain", Threshold, MinMax)
    self.Weather = Weather() 
    self.Analogic = False
    self.Value = self.Weather.GetRain()

  def Update(self, Value = ""):
    self.Weather.Update()
    Sensor.Update(self,self.Weather.GetRain())
    
  def Check(self):
    self.Weather.Update()
    return Sensor.Check(self)

class FogSensor(Sensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    Sensor.__init__(self, "fog", Threshold, MinMax)
    self.Weather = Weather() 
    self.Analogic = False
    self.Value = self.Weather.GetFog()

  def Update(self, Value = ""):
    self.Weather.Update()
    Sensor.Update(self,self.Weather.GetFog())
    
  def Check(self):
    self.Weather.Update()
    return Sensor.Check(self)

class SnowSensor(Sensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    Sensor.__init__(self, "snow", Threshold, MinMax)
    self.Weather = Weather() 
    self.Analogic = False
    self.Value = self.Weather.GetSnow()

  def Update(self, Value = ""):
    self.Weather.Update()
    Sensor.Update(self,self.Weather.GetSnow())
    
  def Check(self):
    self.Weather.Update()
    return Sensor.Check(self)

class CloudsSensor(Sensor):
  def __init__(self, Threshold, MinMax, Argument3 = "", Argument4 = ""):
    Sensor.__init__(self, "clouds", Threshold, MinMax)
    self.Weather = Weather() 
    self.Analogic = False
    self.Value = self.Weather.GetClouds()

  def Update(self, Value = ""):
    self.Weather.Update()
    Sensor.Update(self,self.Weather.GetClouds())
    
  def Check(self):
    self.Weather.Update()
    return Sensor.Check(self)
