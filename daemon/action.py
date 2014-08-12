#!/usr/bin/python
import httplib
import urllib

class Action:
 def __init__(self):
  raise NotImplementedError
 
 def Action(self):
  raise NotImplementedError

class ArduinoAction(Action):
  def __init__(self, Command, Argument= ""):
    self.Command = Command
    self.Argument = Argument

  def Action(self):
    return str(self.Command) + ":" + str(self.Argument) + '\n'

class PushOverAction(Action):
  def __init__(self, Title = "NO TITLE", Message = "NO MESSAGE", Priority = -2):

    self.Title = Title
    self.Message = Message
    self.Priority = Priority
    return
  
  def Action(self):  
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
      "token": "aSc5CqmfEq4ERGQpMqUT7UyyQ4SiJv",
      "user": "u5didSoEPW9xCDpnYoKV85X655ayjc",
      "title": self.Title,
      "message": self.Message,
      "priority": self.Priority
      }), { "Content-type": "application/x-www-form-urlencoded" })
    Answer = conn.getresponse()
    return ""
