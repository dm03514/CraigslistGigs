from craigslist_gigs.utils import Email
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class GigPipeline(object):

  def __init__(self):
    dispatcher.connect(self.spider_closed, signals.spider_closed)

  def spider_closed(self, spider):
    if spider.relevant_gigs_list:
      new_email = Email(spider.relevant_gigs_list)
      new_email.send()
