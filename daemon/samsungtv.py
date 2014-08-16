#!/usr/bin/python
import time
import socket
import base64
import fcntl
import struct
from action import *
from config import *


class SamsungTvAction(Action):
  def __init__(self, Keys, Arg2  = "", Arg3 = "", Arg4 = "", Arg5 = ""):
    Config = Configuration()
    self.Keys = Keys
    self.Mac = self.GetIPAddress("eth0")
    self.SrcIP = self.GetMACAddress("eth0")
    self.DstIP = str(Config.GetKey("SamsungTV", "IP"))
    self.Remote = "Maison Remote"
    self.App = 'python'            # iphone..iapp.samsung
    self.Tv = 'UE46Di5700'          # iphone.LE32C650.iapp.samsung

  def GetIPAddress(self, IfName):
    S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(S.fileno(),
      0x8915,  # SIOCGIFADDR
      struct.pack('256s', IfName[:15]))[20:24])

  def GetMACAddress(self, IfName):
    S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(S.fileno(), 0x8927,  struct.pack('256s', IfName[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

  def Push(self, Key):
    try:
      S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      S.connect((self.DstIP, 55000))
      Msg = chr(0x64) + chr(0x00) +\
        chr(len(base64.b64encode(self.SrcIP)))    + chr(0x00) + base64.b64encode(self.SrcIP) +\
        chr(len(base64.b64encode(self.Mac)))    + chr(0x00) + base64.b64encode(self.Mac) +\
        chr(len(base64.b64encode(self.Remote))) + chr(0x00) + base64.b64encode(self.Remote)
      Pkt = chr(0x00) +\
        chr(len(self.App)) + chr(0x00) + self.App +\
        chr(len(Msg)) + chr(0x00) + Msg
      S.send(Pkt)
      Msg = chr(0x00) + chr(0x00) + chr(0x00) +\
        chr(len(base64.b64encode(Key))) + chr(0x00) + base64.b64encode(Key)
      Pkt = chr(0x00) +\
        chr(len(self.Tv))  + chr(0x00) + self.Tv +\
        chr(len(Msg)) + chr(0x00) + Msg
      S.send(Pkt)
      S.close()
      time.sleep(0.1)
    except:
      return

  def Action(self):
    for Key in self.Keys.split(','):
      self.Push(Key)
