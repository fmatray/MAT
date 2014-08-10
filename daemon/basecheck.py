#!/usr/bin/python

class Action:
  def __init__(self, Command, Argument= ""):
    self.Command = Command
    self.Argument = Argument

  def Action(self):
    return str(self.Command) + ":" + str(self.Argument) + '\n'

class BaseCheck:
  ActionList = []
  def __init__(self, Command = "", Argument = ""):
    if Command != "":
      self.AddAction(Command, Argument)

  def AddAction(self, Command, Argument = ""):
    self.ActionList.append(Action(Command, Argument))

  def Action(self):
    ActionCommand = ""
    for Action in self.ActionList:
      ActionCommand += Action.Action()
    return ActionCommand

  def IsSensor(self):
    return False
