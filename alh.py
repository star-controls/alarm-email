
import pandas
from channel import channel
from mail import mail

class alh(object):
   #_____________________________________________________________________________
   def __init__(self):
      self.mail = mail()
      self.chlist = []
      self.conf = pandas.read_csv("alhconf.csv")
      for i in range(len(self.conf)):
         self.chlist.append(channel(self.conf["channel"][i], self.conf["description"][i], self.mail))

   #_____________________________________________________________________________
   def show(self):
      for i in range(len(self.chlist)):
         print i, ":", self.chlist[i].pvname, ",", self.chlist[i].desc, ", masked: ", self.chlist[i].is_masked

   #_____________________________________________________________________________
   def set_mask(self, i):
      self.chlist[i].is_masked = True

   #_____________________________________________________________________________
   def clear_mask(self, i):
      self.chlist[i].is_masked = False

   #_____________________________________________________________________________
   def quit(self):
      print "Bye"

