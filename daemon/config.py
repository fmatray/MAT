#!/usr/bin/python

class Config:
  def __init__(self):
    self.Config = dict()
    return

  def AddKey(self, Category, Key, Value):
    if (self.Config.has_key(Category) == False):
      self.Config[Category] = dict()
    self.Config[Category][Key] = Value

  def GetKey(self, Category, Key):
    if (self.Config.has_key(Category) == False or self.Config[Category].has_key(Key) == False):
      return None
    return self.Config[Category][Key]

  def Show(self):
    print self.Config
