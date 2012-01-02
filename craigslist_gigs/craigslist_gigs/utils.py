from craigslist_gigs import settings
import smtplib

class Email:
  
  def __init__(self, matches_list):
    """
    Must contain a list of Gig items
    """
    self.message = ''
    for gig in matches_list:
      self.message += '%s - %s - %s\n' % (gig['name'], gig['url'], ','.join(gig['skills']))

  def send(self):
    """
    Send an email.
    """
    gmail_user = settings.EMAIL_USER
    gmail_pwd = settings.EMAIL_PASSWORD 
    smtpserver = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + settings.TO_EMAIL + '\n' + 'From: ' + gmail_user + '\n' + 'Craigslist:Jobs' + '\n'
    msg = header + '\n' + self.message + '\n\n'
    smtpserver.sendmail(gmail_user, settings.TO_EMAIL, msg)
    smtpserver.close()

