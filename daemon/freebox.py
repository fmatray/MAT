#!/usr/bin/python
import urllib2 
from action import *
from config import *

class FreeboxAction(Action):
  def __init__(self, Keys, Arg2 = "", Arg3 = "", Arg4 = "", Arg5 = ""):
    Config = Configuration()
    self.Keys = Keys
    self.RemoteCode = str(Config.GetKey("Freebox", "Code"))
    
  def Push(self, Key):
    try:
      urllib2.urlopen("http://hd1.freebox.fr/pub/remote_control?key=" + Key + "&code=" + self.RemoteCode)
    except URLError, e:
      logging.info("Cannot connect to the freebox player")
      pass
  def Action(self):
    for Key in self.Keys.split(','):
      self.Push(Key)
