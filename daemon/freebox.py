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
      URL = "http://hd1.freebox.fr/pub/remote_control?key=" + Key + "&code=" + self.RemoteCode
      Answer = urllib2.urlopen(URL)
      if Answer.getcode() != 200:
        logging.warning("Error with the freebox player : " + Answer.getcode())
        logging.warning("URL : " + URL)
    except URLError, e:
      logging.warning("Cannot connect to the freebox player")
      pass
  def Action(self):
    if self.RemoteCode == None:
      logging.warning("No remote code specified")
      return
    for Key in self.Keys.split(','):
      self.Push(Key)
