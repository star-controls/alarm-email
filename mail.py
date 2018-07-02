
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pandas
from datetime import datetime

class mail(object):
   #_____________________________________________________________________________
   def __init__(self):
      self.login_file = "login.csv"
      self.subscribers_file = "subscribers.csv"

   #_____________________________________________________________________________
   def put_msg(self, msg_text):

      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()

      login = pandas.read_csv(self.login_file)
      server.login(login["login"][0], login["pwd"][0])

      msg_time = ", time: " + str(datetime.now()).split(".")[0]
      msg_text += msg_time

      maillist = pandas.read_csv(self.subscribers_file)
      for imail in range(len(maillist)):
         msg = MIMEMultipart()
         sendfrom = login["login"][0]
         sendto = maillist["address"][imail]
         msg['From'] = sendfrom
         msg['To'] = sendto
         msg['Subject'] = "STAR Alarm Handler"
         msg.attach(MIMEText(msg_text, 'plain'))
         server.sendmail(sendfrom, sendto, msg.as_string())
      print msg_text

      server.quit()



























