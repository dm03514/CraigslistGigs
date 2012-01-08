from craigslist_gigs import settings
from craigslist_gigs.utils import Email
from datetime import datetime
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import sqlite3

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class GigPipeline(object):
  """This isn't using pipelines correctly could be refactored to do so."""

  def __init__(self):
    dispatcher.connect(self.spider_closed, signals.spider_closed)
    self.connection = sqlite3.connect(settings.DATABASE_NAME)
    self.cursor = self.connection.cursor()

  def spider_closed(self, spider):
    #import ipdb; ipdb.set_trace()
    unsent_gigs_list = self.check_gigs_sent(spider.relevant_gigs_list)
    if unsent_gigs_list:
      new_email = Email(unsent_gigs_list)
      new_email.send()
      # loop back through and save each one as sent.
      self.record_sent_gigs(unsent_gigs_list)
      self.cursor.close()

  def record_sent_gigs(self, unsent_gigs_list):
    """
    Save that these gigs were notified so they don't show up in every email.
    """
    query = 'INSERT INTO gigs values (?, ?, ?, ?, ?)'
    for gig in unsent_gigs_list:
      self.cursor.execute(query, (
        gig['name'],
        gig['url'],
        ','.join(gig['skills']),
        datetime.now(),
        True
      ))
      self.connection.commit()

  def check_gigs_sent(self, relevant_gigs_list):
    """
    Check to see if these were already emailed.
    """
    unsent_gigs_list = []
    query = 'SELECT COUNT(*) FROM gigs WHERE url=?'
    for gig in relevant_gigs_list:
      self.cursor.execute(query, (gig['url'],))
      already_sent = self.cursor.fetchone()[0]
      if not already_sent:
        unsent_gigs_list.append(gig)  
    return unsent_gigs_list
