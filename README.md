### **CraigslistGigs**: Scrapy project that searches HTML/creative gigs on Craigslist for jobs!

This requires a list of cities to search for and a list of skills.  The cities must be valid Craigslist cities.  It will then search all computer gigs in those cities for any gigs which contain your skills.  It will email you all the gigs that have not yet been mailed to you.  It keeps track of gigs in a sqlite database named db_gigs.db located in the same directory as `settings.py`.

### Dependencies
  *  Scrapy (`pip install scrapy` | `pip3 install scrapy`)
  *  `requirements.txt` has Scrapy version and versions of all components


### Usage
  * Create a `db_gigs.db` file in the same directory as `settings.py`
  * CREATE TABLE gigs(name text, url text, skills text, gig_datetime datetime, sent boolean);
  * Scrapy `settings.py` file must exist with the constants `EMAIL_USER`, `EMAIL_PASSWORD`, `TO_EMAIL`, `SMTP_SERVER`, `SMTP_PORT`
  * Make sure you populate `settings.MY_SKILLS_LIST` with your relevant skills
  * settings.CITIES_LIST must have a list of cities.  These are used to create Craigslist urls, of the form http://cityname.craigslist.org. Make sure they are valid
  * `scrapy crawl gigs`

Each computer gig found in the cities list will be checked to see if it contains any of you listed skills.




The email that is sent is very simple. For example:

```
Need a skilled IPB Forum/IP.Content programmer (Alexandria, Virginia) - http://washingtondc.craigslist.org/nva/cpg/3522913878.html - php,html
Junior Software Engineer / Web programmer (Massapequa, NY) - http://newyork.craigslist.org/lgi/cpg/3512399543.html - php,css,html
Graphic Position (Ronkonkoma) - http://newyork.craigslist.org/lgi/cpg/3485356110.html - javascript
Website Developer (N/A) - http://newyork.craigslist.org/stn/cpg/3476870457.html - php,css,html,javascript
Professional Website Developer (N/A) - http://newyork.craigslist.org/stn/cpg/3476881527.html - php,css,html,javascript
Front-End Developer Needed (Westchester NY) - http://newyork.craigslist.org/wch/cpg/3473266282.html - css,html,javascript
Web Developer (Port Chester, NY) - http://newyork.craigslist.org/wch/cpg/3533739219.html - php,css,html,javascript
```

It includes the Post Title, Link, and the Skills that the post contains.
