#!/usr/bin/python
import imaplib
import poplib

class Email:
  def __init__(self, Command, Argument):
    self.Command = Command
    self.Argument = Argument

  def Action(self):
    return str(self.Command) + ":" + str(self.Argument)

class ImapEmail(Email):
  Server = ""
  Port = 0
  Login = ""
  Password = "" 
  Ssl = 0
  LastUnReadCount = 0
  LastMessagesCount = 0
  def __init__(self, Server, Port, Login, Password, Ssl, Command, Argument):
    Email.__init__(self, Command, Argument)
    if Port == 0:
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
      print "CANNOT OPEN " + self.Server
      raise
  
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

class PopEmail(Email):
  Server = "" 
  Port = 0
  Login = ""
  Password = "" 
  Ssl = 0
  LastMessagesCount = 0
  def __init__(self, Server, Port, Login, Password, Ssl, Commannd, Argument):
    Email.__init__(self, Commannd, Argument)
    if Port == 0:
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
      print "CANNOT OPEN " + self.Server
      raise

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
