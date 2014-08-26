#!/usr/bin/python

from pyicloud import PyiCloudService
from config import *
from geopy.distance import vincenty

class ICloud(object):
  _Instance = None
  Configured = False
   
  def __new__(cls):
    if ICloud._Instance == None:
      ICloud._Instance = object.__new__(cls)
      return ICloud._Instance
  
  def __init__(self):
    if self.Configured == True:
      return
    try:
      Config = Configuration()
      self.User = config.Config.GetKey("ICloud", "User")
      self.Password = config.Config.GetKey("ICloud", "Password")
      self.Device = config.Config.GetKey("ICloud", "Device")
      Self.Api = PyiCloudService(self.User, self.Password)
    except:
      raise

  def GetLocation(self):
    Location = self.Api.iphone.location()
    if Location["locationFinished"] == True and Location["positionType"] == "GPS":
      return (Location["longitude"], Location["latitude"])
    else:
      return None

class ICalendar(Sensor):
  def __init__(self, Argument1 = "", Argument2 = "", Argument3 = "", Argument4 = ""):
    self.Icloud = Icloud()
    
  def Update(self):
    raise NotImplementedError
    return
    
  def Check(self):
    raise NotImplementedError
    return
    
class IDeviceLocation(Sensor):
  def __init__(self, Longitude, Latitude, Argument3 = "", Argument4 = ""):
    self.Icloud = Icloud()
    self.Target = (Longitude, Latitude)
    self.LastUpdateTime = None
    
  def Update(self):
    if self.LastUpdateTime == None or (datetime.datetime.now() - self.LastUpdateTime).seconds >= 120 :
      self.Location = self.ICloud.GetLocation()
      self.LastUpdateTime = datetime.datetime.now() 
    
  def Check(self):
    self.Update()
    if self.Location != None and vincenty(self.Target, self.Location).meters < 300:
      self.Action()
    
