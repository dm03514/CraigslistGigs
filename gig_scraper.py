from BeautifulSoup import BeautifulSoup
import config
import re
import smtplib
from urllib import urlopen

def main():
  gig_areas_list = [
    'baltimore',
    'washingtondc',
  ]
  gig_urls_list = get_posting_urls(gig_areas_list)
  get_relevent_gigs(gig_urls_list)

def get_posting_urls(gig_areas_list):
  """
  Scrape a list of gig urls for relevent freelance gigs.
  @return list gig urls
  """
  for gig_area in gig_areas_list:
    url = 'http://%s.craigslist.org/cpg/' % (gig_area)
    f = urlopen(url)
    soup = BeautifulSoup(f.read())
    # Get just the postings
    posting_urls_result_set = soup.findAll('a', href=re.compile(url+'\d+.html'))
    # combine all areas instead of returning right here
    return [tag.attrs[0][1] for tag in posting_urls_result_set]
    
def get_relevent_gigs(gig_urls_list):
  """
  Get postings that contain any of my skills.  Requires a list of posting urls to try.
  @return 
  """
  import ipdb; ipdb.set_trace()
  my_skills_list = ['php', 'python', 'django', 'css', 'html', 'javascript',]
  matches_list = []
  for gig_url in gig_urls_list:
    f = urlopen(gig_url)
    soup = BeautifulSoup(f.read())
    body_str = soup.find('div', id='userbody').text.lower()
    gig_dict = {'url': gig_url, 'skills': []}
    for skill in my_skills_list:
      if skill in body_str:
        gig_dict['skills'].append(skill)
    if gig_dict['skills']:
      matches_list.append(gig_dict) 
  if matches_list:
    send_email(matches_list)

def send_email(matches_list):
  """
  Send an email with any matching gigs.
  """
  to = 'dm03514@gmail.com'
  gmail_user = ''
  gmail_pwd = ''
  smtpserver = smtplib.SMTP("smtp.gmail.com",587)
  smtpserver.ehlo()
  smtpserver.starttls()
  #smtpserver.ehlo
  smtpserver.login(gmail_user, gmail_pwd)
  header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
  print header
  msg = header + '\n this is test msg from mkyong.com \n\n'
  smtpserver.sendmail(gmail_user, to, msg)
  print 'done!'
  smtpserver.close()

if __name__ == '__main__':
  main() 
