from craigslist_gigs import settings
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
  return ['http://baltimore.craigslist.org/cpg/3693954402.html']
  full_urls_list = []
  for city in settings.CITIES_LIST:
    full_urls_list.append('http://%s.craigslist.org' % (city))
  return full_urls_list


class GigSpider(CrawlSpider):
  name = 'gigs'
  start_urls = get_start_urls()

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

    content = ','.join((item.strip() for item in hxs.select('//section[@id="postingbody"]/text()').extract()))
    title_parts_list = hxs.select('//h2[@class="postingtitle"]/text()').extract()
    title = ','.join(x.strip() for x in title_parts_list if x.strip())
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
    for skill in settings.MY_SKILLS_LIST:
      if skill in content.lower():
        matches_list.append(skill)
    return matches_list
