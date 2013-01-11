import os
# Scrapy settings for craigslist_gigs project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'craigslist_gigs'

SPIDER_MODULES = ['craigslist_gigs.spiders']
NEWSPIDER_MODULE = 'craigslist_gigs.spiders'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:8.0.1) Gecko/20100101 Firefox/8.0.1'

ITEM_PIPELINES = [
  'craigslist_gigs.pipelines.GigPipeline',
]

TO_EMAIL = ''
EMAIL_USER = ''
EMAIL_PASSWORD = ''
SMTP_SERVER = ''
SMTP_PORT = '' 

PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)))

DATABASE_NAME = os.path.join(PROJECT_ROOT, 'db_gigs.db')

try:
    from settings_local import *
except ImportError:
    pass
