#!/usr/bin/python
from  action import *

class BaseCheck:
  def __init__(self):
    self.ActionList = []
    return 
  def AddAction(self, Act):
    self.ActionList.append(Act)

  def Action(self):
    ActionCommand = ""
    for Action in self.ActionList:
      Action.Action()

  def IsSensor(self):
    return False
