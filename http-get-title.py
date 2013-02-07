#!/usr/bin/env python

import sys
import urllib2
import HTMLParser

class TitleParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.in_header = False

    def handle_starttag(self, tag, attrs):
        headerList = ['h1','h2','h3','h4','h5','h6']
        if tag in headerList:
            self.in_header = True

    def handle_endtag(self, tag):
        headerList = ['h1','h2','h3','h4','h5','h6']
        if tag in headerList:
            self.in_header = False

    def handle_data(self, data):
        if self.in_header:
            print data

parser = TitleParser()

for url in sys.argv[1:]:
    f = urllib2.urlopen(url)
    parser.feed(f.read())
    f.close()

