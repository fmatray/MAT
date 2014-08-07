#!/usr/bin/python

class BaseCheck:
  def __init__(self, Command, Argument):
    self.Command = Command
    self.Argument = Argument

  def Action(self):
    return str(self.Command) + ":" + str(self.Argument) + '\n'
