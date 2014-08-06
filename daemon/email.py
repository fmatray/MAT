#!/usr/bin/python
import imaplib
import poplib

class ImapEmail:
  server = ""
  port = 0
  login = ""
  password = "" 
  ssl = 0
  LastUnReadCount = 0
  LastMessagesCount = 0
  def __init__(self, server, port, login, password, ssl):
    if port == 0:
      if ssl == True:
        port = 993
      else:
        port = 143
    self.server = server
    self.port = port
    self.login = login
    self.password = password
    self.ssl = ssl
    self.OpenConnection()
  
  def OpenConnection(self):
    try:
      if self.ssl == True:
        self.Mail = imaplib.IMAP4_SSL(self.server, self.port)
      else:
        self.Mail = imaplib.IMAP4(self.server, self.port)
      (RetCode, Capabilities) = self.Mail.login(self.login, self.password)
      if RetCode == "OK":
        self.Mail.select()
    except Exception, e:
      print "CANNOT OPEN " + self.server
      raise
  
  def Check(self):
    try:
      type, data= self.Mail.status('INBOX', '(UNSEEN)')
      UnReadCount = int(data[0].split()[2].strip(').,]'))
      type, data= self.Mail.status('INBOX', '(MESSAGES)')
      MessagesCount = int(data[0].split()[2].strip(').,]'))
      Ret = False
      if MessagesCount > self.LastMessagesCount and UnReadCount > self.LastUnReadCount:
        Ret = True 
      self.LastUnReadCount = UnReadCount
      self.LastMessagesCount = MessagesCount
      return Ret
    except:
      self.OpenConnection()
      return False

class PopEmail:
  server = "" 
  port = 0
  login = ""
  password = "" 
  ssl = 0
  LastMessagesCount = 0
  def __init__(self, server, port, login, password, ssl):
    if port == 0:
      if ssl == True:
        port = 995
      else:
        port = 110
    self.server = server
    self.port = port
    self.login = login
    self.password = password
    self.ssl = ssl
    self.OpenConnection()

  def OpenConnection(self):
    try:
      if self.ssl == True:
        self.Mail = poplib.POP3_SSL(self.server, self.port)
      else:
        self.Mail = poplib.POP3(self.server, self.port)
      self.Mail.getwelcome()
      self.Mail.user(self.login)
      self.Mail.pass_(self.password)
      (MessagesCount, MailboxSize) =  self.Mail.stat()
    except Exception, e:
      print "CANNOT OPEN " + self.server
      raise

  def Check(self):
    Ret = False
    try:
      self.Mail.quit()
      self.OpenConnection()
      (MessagesCount, MailboxSize) =  self.Mail.stat()
      print str(MessagesCount) + " "+ str(self.LastMessagesCount)
      if MessagesCount > self.LastMessagesCount:
        Ret = True
      self.LastMessagesCount = MessagesCount
      self.Mail.stat()
      return Ret
    except:
      self.OpenConnection()
      return False
