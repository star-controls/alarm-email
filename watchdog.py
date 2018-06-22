
import threading
import time

class watchdog(object):
   #_____________________________________________________________________________
   def __init__(self, timeout, handler):
      self.timeout = timeout
      self.handler = handler
      self.tid = threading.Thread(target=self.loop)
      self.tid.daemon = True
      self.tid.start()
   #_____________________________________________________________________________
   def loop(self):
      while True:
         time.sleep(self.timeout)
         self.handler()


