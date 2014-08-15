#!/usr/bin/python

class Configuration(object):
  _Instance = None
  Config = dict()
  def __new__(cls):
    if Configuration._Instance == None:
      Configuration._Instance = object.__new__(cls)
    return Configuration._Instance

  def __init__(self):
    global Config
    Config = self
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
    for CategoryKey in self.Config:
      for KeyKey in self.Config[CategoryKey]:
        print CategoryKey + ":" + KeyKey + ":"  + self.Config[CategoryKey][KeyKey]

