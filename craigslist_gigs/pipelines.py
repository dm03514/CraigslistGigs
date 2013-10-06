from datetime import datetime
import sqlite3

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem

from craigslist_gigs import settings
from craigslist_gigs.utils import Email, check_gig_for_skills


# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class GigPipeline(object):
    """This isn't using pipelines correctly could be refactored to do so."""

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.connection = sqlite3.connect(settings.DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.gigs_to_send = []

    def process_item(self, gig, spider):
        """
        Check if a gig contains the correct skills, and keeps track of it for
        later if it does
        """
        # check if gig has the correct skills
        matching_skills = check_gig_for_skills(gig['content'])
        if not matching_skills:
            return DropItem('No matching skills: {}'.format(gig['url']))

        gig['skills'] = matching_skills

        # check if gig has already been saved
        query = 'SELECT COUNT(*) FROM gigs WHERE url=?'
        self.cursor.execute(query, (gig['url'],))
        already_sent = self.cursor.fetchone()[0]
        if already_sent:
            return DropItem('Gig Already Sent: {}'.format(gig['url']))

        self.gigs_to_send.append(gig) 

    def spider_closed(self, spider):
        """
        Email all the gigs that should be sent, and record that they were sent.
        """
        new_email = Email()
        message = new_email.build_message_from_gigs(self.gigs_to_send)
        new_email.send(settings.TO_EMAIL, message)
        # loop back through and save each one as sent.
        self.record_sent_gigs(self.gigs_to_send)
        self.cursor.close()

    def record_sent_gigs(self, gigs_list):
        """
        Save that these gigs were notified so they don't show up in every email.
        """
        query = 'INSERT INTO gigs values (?, ?, ?, ?, ?)'
        for gig in gigs_list:
            self.cursor.execute(query, (
                gig['name'],
                gig['url'],
                ','.join(gig['skills']),
                datetime.now(),
                True
            ))
        self.connection.commit()
