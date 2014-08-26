#!/usr/bin/python
from  action import *

class BaseCheck:
  def __init__(self):
    self.ActionList = []
    return 
  def AddAction(self, Act):
    self.ActionList.append(Act)

  def Action(self):
    for Action in self.ActionList:
      Action.Action()

  def IsSensor(self):
    return False

  def Update(self):
    raise NotImplementedError
    
  def Check(self):
    raise NotImplementedError
