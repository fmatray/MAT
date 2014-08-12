#!/usr/bin/python
from  action import *

class BaseCheck:
  ActionList = []
  def __init__(self):
    return 
  def AddAction(self, Act):
    self.ActionList.append(Act)

  def AddArduinoAction(self, Command, Argument = ""):
    if Command != "":
      self.ActionList.append(Action(Command, Argument))

  def AddPushOverAction(self, Title, Message = "", Priority = -2):
    if Title != "":
      self.ActionList.append(PushOver(Title, Message, Priority))

  def Action(self):
    ActionCommand = ""
    for Action in self.ActionList:
      ActionCommand += Action.Action()
    return ActionCommand

  def IsSensor(self):
    return False
