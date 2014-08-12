#!/usr/bin/python
import httplib
import urllib

class Action:
  def __init__(self, Command, Argument= ""):
    self.Command = Command
    self.Argument = Argument

  def Action(self):
    return str(self.Command) + ":" + str(self.Argument) + '\n'

class PushOver(Action):
  def __init__(self, Title = "NO TITLE", Message = "NO MESSAGE", Priority = -2):

    self.Title = Title
    self.Message = Message
    self.Priority = Priority
    return
  
  def Action(self):  
    print "Push Over"
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
      "token": "aFsunBbSxoDitr9DbfAqGWTtLTKmYc",
      "user": "u5didSoEPW9xCDpnYoKV85X655ayjc",
      "title": self.Title,
      "message": self.Message,
      "priority": self.Priority
      }), { "Content-type": "application/x-www-form-urlencoded" })
    Answer = conn.getresponse()
    print Answer.getheaders()
    print Answer.read()
    return ""
