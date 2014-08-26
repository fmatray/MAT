#!/usr/bin/python
import time
import datetime
import sys
import copy

class Schedule:
  def __init__(self, DataBase):
    try:
      self.CheckList = list()
      self.LocalTime = datetime.datetime.now()
      self.LastCheck = self.LocalTime
      self.CheckList = DataBase.InitElements()
    except Exception, e:
      raise

  def Update(self):
    for Element in self.CheckList:
      Element.Update()
      
  def Check(self):
    for Element in self.CheckList:
      Element.Check()

  def Schedule(self):
    self.Update()
    self.LocalTime = datetime.datetime.now()
    if self.LocalTime.second <= 10 and (self.LocalTime - self.LastCheck).seconds > 10:
      self.Check()
      self.LastCheck = self.LocalTime

