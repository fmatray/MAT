#!/usr/bin/python
import imaplib
import poplib
import logging
from sensor import *

class ImapEmailSensor(Sensor):
  def __init__(self, ServerPort, Login, Password, Ssl):
    Sensor.__init__(self)
    (Server, Port) = ServerPort.split(":")
    if Port == "":
      if Ssl == True:
        Port = 993
      else:
        Port = 143
    self.Server = Server
    self.Port = Port
    self.Login = Login
    self.Password = Password
    self.Ssl = Ssl
    self.OpenConnection()
    self.LastUnReadCount = 0
    self.LastMessagesCount = 0
  
  def OpenConnection(self):
    try:
      if self.Ssl == True:
        self.Mail = imaplib.IMAP4_SSL(self.Server, self.Port)
      else:
        self.Mail = imaplib.IMAP4(self.Server, self.Port)
      (RetCode, Capabilities) = self.Mail.login(self.Login, self.Password)
      if RetCode == "OK":
        self.Mail.select()
    except Exception, e:
      logging.error("CANNOT OPEN " + self.Server)
  
  def Update(self):
    self.Mail.noop()
  
  def Check(self):
    try:
      Type, Data= self.Mail.status('INBOX', '(UNSEEN)')
      UnReadCount = int(Data[0].split()[2].strip(').,]'))
      Type, Data= self.Mail.status('INBOX', '(MESSAGES)')
      MessagesCount = int(Data[0].split()[2].strip(').,]'))
      Ret = ""
      if MessagesCount > self.LastMessagesCount and UnReadCount > self.LastUnReadCount:
        Ret = self.Action() 
      self.LastUnReadCount = UnReadCount
      self.LastMessagesCount = MessagesCount
      return Ret
    except:
      self.OpenConnection()
      return ""

class PopEmailSensor(Sensor):
  def __init__(self, ServerPort, Login, Password, Ssl):
    Sensor.__init__(self)
    (Server, Port) = ServerPort.split(":")
    if Port == "":
      if Ssl == True:
        Port = 995
      else:
        Port = 110
    self.Server = Server
    self.Port = Port
    self.Login = Login
    self.Password = Password
    self.Ssl = Ssl
    self.OpenConnection()
    self.LastMessagesCount = 0

  def OpenConnection(self):
    try:
      if self.Ssl == True:
        self.Mail = poplib.POP3_SSL(self.Server, self.Port)
      else:
        self.Mail = poplib.POP3(self.Server, self.Port)
      self.Mail.getwelcome()
      self.Mail.user(self.Login)
      self.Mail.pass_(self.Password)
      (MessagesCount, MailboxSize) =  self.Mail.stat()
    except Exception, e:
      logging.error("CANNOT OPEN " + self.Server)

  def Update(self):
    self.Mail.noop()
  
  def Check(self):
    Ret = ""
    try:
      self.Mail.quit()
      self.OpenConnection()
      (MessagesCount, MailboxSize) =  self.Mail.stat()
      if MessagesCount > self.LastMessagesCount:
        Ret = self.Action()
      self.LastMessagesCount = MessagesCount
      self.Mail.stat()
      return Ret
    except:
      self.OpenConnection()
      return ""
