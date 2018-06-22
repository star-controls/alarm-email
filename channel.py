
import time
import threading
from epics import PV, caget
from watchdog import watchdog

class channel(object):
   #from EPICS BASE alarmString.h:
   epicsAlarmSeverityStrings = ["NO_ALARM", "MINOR", "MAJOR", "INVALID"]
   epicsAlarmConditionStrings = [
    "NO_ALARM",
    "READ",
    "WRITE",
    "HIHI",
    "HIGH",
    "LOLO",
    "LOW",
    "STATE",
    "COS",
    "COMM",
    "TIMEOUT",
    "HWLIMIT",
    "CALC",
    "SCAN",
    "LINK",
    "SOFT",
    "BAD_SUB",
    "UDF",
    "DISABLE",
    "SIMM",
    "READ_ACCESS",
    "WRITE_ACCESS"
   ]
   #_____________________________________________________________________________
   def __init__(self, pvname, desc, mail):
      self.mail = mail
      self.desc = desc
      self.pvname = pvname
      self.initialized = False
      self.sevr_val = 0
      self.alarm_flag = False
      self.msg_counter = 0
      self.max_msg = 4
      self.max_msg_reached = False
      self.is_masked = False
      self.stat_pv = PV(self.pvname+".STAT")
      self.val_pv = PV(self.pvname+".VAL")
      self.sevr_pv = PV(self.pvname+".SEVR", callback=self.on_sevr_change, connection_callback=self.on_connection_change)
      if self.sevr_pv.status is None:
         self.initialized = True
         self.on_connection_change(False)
      self.wdt = watchdog(3600, self.reset_max_msg)
      self.tid = threading.Thread(target=self.monit_loop)
      self.tid.daemon = True
      self.tid.start()
   #_____________________________________________________________________________
   def on_sevr_change(self, value=None, **kw):
      if self.initialized == False:
         self.initialized = True
         if value == 0:
            return
      if self.is_masked == True or self.max_msg_reached == True:
         return
      self.sevr_val = value
      self.alarm_flag = True

   #_____________________________________________________________________________
   def put_msg(self, msg):
      self.mail.put_msg(msg)

   #_____________________________________________________________________________
   def set_alarm(self):
      if self.msg_counter >= self.max_msg:
         msg = "Warning in '" + self.desc + "', "
         msg += "maximal number of alarms per hour exceeded"
         self.msg_counter += 1
         self.put_msg(msg)
         self.max_msg_reached = True
         return
      msg = "Alarm "
      if self.sevr_val == 0:
         msg += "cleared"
      else:
         msg += "raised"
      msg += " in '" + self.desc + "', "
      msg += self.epicsAlarmConditionStrings[self.stat_pv.get()] + ", "
      msg += self.epicsAlarmSeverityStrings[self.sevr_val] + ", value: "
      msg += str(self.val_pv.get())
      self.msg_counter += 1
      self.put_msg(msg)

   #_____________________________________________________________________________
   def alarm_monit(self):
      if self.alarm_flag == True:
         self.set_alarm()
         self.alarm_flag = False

   #_____________________________________________________________________________
   def monit_loop(self):
      while True:
         time.sleep(0.1)
         self.alarm_monit()

   #_____________________________________________________________________________
   def reset_max_msg(self):
      self.msg_counter = 0
      self.max_msg_reached = False
      
   #_____________________________________________________________________________
   def on_connection_change(self, conn=None, **kw):
      #if self.connection_init == False:
         #self.connection_init = True
      if self.is_masked == True or self.max_msg_reached == True:
         return
      if conn == True:
         return
      self.put_msg("Alarm raised in '"+self.desc+"', channel disconnected")




















