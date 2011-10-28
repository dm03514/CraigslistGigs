from BeautifulSoup import BeautifulSoup
from cookielib import CookieJar
import re
from urllib import urlopen
import urllib2

def main():
  gig_areas_list = [
    'baltimore',
    'washingtondc',
  ]
  get_posting_urls(gig_areas_list)

def get_posting_urls(gig_areas_list):
  """
  Scrape a list of gig urls for relevent freelance gigs.
  """
  for gig_area in gig_areas_list:
    url = 'http://%s.craigslist.org/cpg/' % (gig_area)
    f = urlopen(url)
    soup = BeautifulSoup(f.read())
    # Get just the postings
    posting_urls_result_set = soup.findAll('a', href=re.compile(url+'\d+.html'))
    gig_urls_list = [tag.attrs[0][1] for tag in posting_urls_result_set]
    get_relevent_gigs(gig_urls_list)

def get_relevent_gigs(gig_urls_list):
  """
  Get postings that contain any of my skills.  Requires a list of posting urls to try.
  """
  import ipdb; ipdb.set_trace()
  my_skills_list = ['php', 'python', 'django', 'css', 'html', 'javascript']
  matches_list = []
  for gig_url in gig_urls_list:
    f = urlopen(gig_url)
    posting_str = f.read().lower()
    gig_dict = {'url': gig_url, 'skills': []}
    for skill in my_skills_list:
      if skill in posting_str:
        gig_dict['skills'].append(skill)
    if gig_dict['skills']:
      matches.append(gig_dict) 
  if matches_list:
    send_email(matches_list)

def send_email(matches_list):
  """
  Send an email with any matching gigs.
  """
  pass

if __name__ == '__main__':
  main() 
