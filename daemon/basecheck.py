#!/usr/bin/python
from  action import *

class BaseCheck:
  ActionList = []
  def __init__(self):
    return 
  def AddAction(self, Act):
    self.ActionList.append(Act)

  def Action(self):
    ActionCommand = ""
    for Action in self.ActionList:
      ActionCommand += Action.Action()
    return ActionCommand

  def IsSensor(self):
    return False
