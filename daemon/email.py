#!/usr/bin/python
import imaplib

class ImapEmail:
  LastUnReadCount = 0
  LastMessagesCount = 0
  def __init__(self, server, login, password):
    self.ImapMail = imaplib.IMAP4_SSL(server)
    (RetCode, Capabilities) = self.ImapMail.login(login, password)
    if RetCode == "OK":
      self.ImapMail.select()
  
  def Check(self):
    print "Check Mail"
    type, data= self.ImapMail.status('INBOX', '(UNSEEN)')
    UnReadCount = int(data[0].split()[2].strip(').,]'))
    type, data= self.ImapMail.status('INBOX', '(MESSAGES)')
    MessagesCount = int(data[0].split()[2].strip(').,]'))
    Ret = False
    if MessagesCount > self.LastMessagesCount and UnReadCount > self.LastUnReadCount:
      Ret = True 
    self.LastUnReadCount = UnReadCount
    self.LastMessagesCount = MessagesCount
    return Ret
