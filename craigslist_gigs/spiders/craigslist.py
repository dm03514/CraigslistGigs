from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from craigslist_gigs import settings
from craigslist_gigs.items import Gig
from craigslist_gigs.utils import get_start_urls 


class GigSpider(CrawlSpider):
    name = 'gigs'
    start_urls = get_start_urls()

    rules = (
        Rule(SgmlLinkExtractor(allow='cpg/$',), follow=True),
        Rule(SgmlLinkExtractor(allow='/\d+\.html$',), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """
        Check body of each individual post, for my skills. 
        This is the callback for actual posts.
        """
        hxs = HtmlXPathSelector(response)

        content = ','.join((item.strip() for item in hxs.select('//section[@id="postingbody"]/text()').extract()))
        title_parts_list = hxs.select('//h2[@class="postingtitle"]/text()').extract()
        title = ','.join(x.strip() for x in title_parts_list if x.strip())
        gig = Gig()
        gig['url'] = response.url
        gig['name'] = title
        gig['content'] = content
        #gig['skills'] = matches_list
        return gig
