#!/usr/bin/python
import httplib
import urllib
from config import *
from arduino import *

class Action:
 def __init__(self):
  raise NotImplementedError
 
 def Action(self):
  raise NotImplementedError

class ArduinoAction(Action):
  Arduino = None
  def __init__(self, Command, Argument= ""):
    if self.Arduino == None:
      self.Arduino = Arduino()
    self.Command = Command
    self.Argument = Argument

  def Action(self):
    self.Arduino.AddOutputData(str(self.Command) + ":" + str(self.Argument) + '\n')

class PushOverAction(Action):
  def __init__(self, Title = "NO TITLE", Message = "NO MESSAGE", Priority = -2):
    Config = Configuration()
    print "______"
    Config.Show()
    print Config
    print "______"
    self.Token = Config.GetKey("PushOver", "Token")
    self.User = Config.GetKey("PushOver", "User")
    if (self.Token == None or self.User == None):
      raise KeyError
    self.Title = Title
    self.Message = Message
    self.Priority = Priority
    return
  
  def Action(self):  
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
      "token": self.Token, 
      "user": self.User, 
      "title": self.Title,
      "message": self.Message,
      "priority": self.Priority
      }), { "Content-type": "application/x-www-form-urlencoded" })
    Answer = conn.getresponse()
