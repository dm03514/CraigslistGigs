from craigslist_gigs.items import Gig
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

def get_start_urls():
  """
  Return all start urls as an iterable, 
  could add db support right now my chosen cities are hardcoded.
  How is the best way to dynamically set a Class attribute? idk
  @return list the list of urls to scrape!
  """
  cities_list = [
    'baltimore',
    'newyork',
    'philadelphia',
    'washingtondc',
  ]
  full_urls_list = []
  for city in cities_list:
    full_urls_list.append('http://%s.craigslist.org' % (city))
  return full_urls_list


class GigSpider(CrawlSpider):
  name = 'gigs'
  start_urls = get_start_urls()

  # used to check listings for matching gigs
  my_skills_list = ['php', 'python', 'django', 'css', 'html', 'javascript',]
  # stores matching gigs so they can be emailed later
  relevant_gigs_list = []

  rules = (
    Rule(SgmlLinkExtractor(allow='cpg/$',), follow=True),
    Rule(SgmlLinkExtractor(allow='/\d+\.html$',), callback='parse_item', follow=True),
  )

  def parse_item(self, response):
    """
    Check body of each individual post, for my skills. This is the callback for actual posts.
    """
    hxs = HtmlXPathSelector(response)
    #import ipdb; ipdb.set_trace()

    content = ','.join((item.strip() for item in hxs.select('//section[@id="userbody"]/text()').extract()))
    title = hxs.select('//h2[@class="postingtitle"]/text()').extract()[0]
    matches_list = self.check_gig_for_skills(content)
    if matches_list:
      gig = Gig()
      gig['url'] = response.url
      gig['name'] = title
      gig['skills'] = matches_list
      self.relevant_gigs_list.append(gig)
      
  def check_gig_for_skills(self, content):
    """
    Check a gig to see if it matches skills.
    @param string content the body of text to check.
    @return list the matching skills or an empty list
    """
    matches_list = []
    for skill in self.my_skills_list:
      if skill in content.lower():
        matches_list.append(skill)
    return matches_list
