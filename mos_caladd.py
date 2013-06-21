#!/usr/bin/env python

# script for adding recurring events to the MOS calendar
# Metalab Operating System (https://github.com/Metalab/mos)

import dateutil.rrule as dr
import dateutil.parser as dparse
import dateutil.relativedelta as drel
import sys
import urllib, urllib2, getpass, time
from cookielib import CookieJar

event =  {
  "category":       "",
  "location":       "1",    #1: Hauptraum, 2: Bibliothek, 7: Lounge (Raucherbetrieb), 
                            # 5: *.*, 6: Woanders, 8: Whateverlab, 9: Kueche, 11: Fotolab, 
                            # 12: any room, 13: heavy machinery, 14: Lounge (Nichtraucherbetrieb)
  "name":           "FunkFeuer",
  "teaser":         "Montagstreffen",
  "wikiPage":       "FunkFeuer",
  "time":           ['19:00', "21:00"],     # ['start', 'end']
  "date":           {
      "freq":         dr.WEEKLY,
      "byweekday":    drel.MO(0),
      "dtstart":      dparse.parse("2013-9-1"),
      "until":        dparse.parse("2013-10-1")
  }
}



BASEURL = 'https://metalab.at'

dates = dr.rrule(**event['date'])
print """Adding new events to calendar:
  Name:\t\t%s
  Teaser:\t%s
  wikiPage:\t%s
  time:\t\t%s to %s
  dates:""" %( event['name'], event['teaser'], 
  event['wikiPage'], event['time'][0], event['time'][1])
print '\t'+'\n\t'.join([d.strftime('%a, %d.%m.%Y') for d in dates])

print '\nusername: ',
username = sys.stdin.readline().rstrip('\n')
password = getpass.getpass('password: ')

posthandler = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()))

data = {    'next'    : '',
            'password': password,
            'username': username}


content = posthandler.open(BASEURL+'/member/login/', data=urllib.urlencode(data)).read()
if ('Please try again' in content):
  print 'Your username and password didn\'t match. Please try again.'
  sys.exit(1)
print 'login successful, adding events:'

eventdata = {
  "category":     event['category'],
  "endDate_1":    event['time'][1],
  "location":     event['location'],
  "name":         event['name'],
  "startDate_1":  event['time'][0],
  "teaser":       event['teaser'],
  "wikiPage":     event['wikiPage'],
}

for d in dates:
  eventdata["startDate_0"]  = d.strftime('%Y-%m-%d')
  eventdata["endDate_0"]    = d.strftime('%Y-%m-%d')
  print ' adding %s...' % d.strftime('%Y-%m-%d'),
  posthandler.open(BASEURL+'/calendar/new/', data=urllib.urlencode(eventdata)).read()
  print 'done.'
  time.sleep(0.1)
print 'added all events.'

