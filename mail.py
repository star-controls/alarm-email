
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pandas

class mail(object):
   #_____________________________________________________________________________
   def __init__(self):
      self.server = smtplib.SMTP('smtp.gmail.com', 587)
      self.server.starttls()
      self.login = pandas.read_csv("login.csv")
      self.server.login(self.login["login"][0], self.login["pwd"][0])

   #_____________________________________________________________________________
   def put_msg(self, msg_text):

      maillist = pandas.read_csv("subscribers.csv")
      for imail in range(len(maillist)):
         msg = MIMEMultipart()
         sendfrom = self.login["login"][0]
         sendto = maillist["address"][imail]
         msg['From'] = sendfrom
         msg['To'] = sendto
         msg['Subject'] = "STAR Alarm Handler"
         msg.attach(MIMEText(msg_text, 'plain'))
         self.server.sendmail(sendfrom, sendto, msg.as_string())
      print msg_text


























