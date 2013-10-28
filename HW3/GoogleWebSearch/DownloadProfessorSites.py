#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis and Jessica Ouyang
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web

import sys, os, getopt
import urllib, urllib2
import json
from bs4 import BeautifulSoup

# I found this hack around for doing a google search from the url below, altered slightly
# http://stackoverflow.com/questions/1657570/google-search-from-a-python-app

def getgoogleurl(search,siteurl=False):
    if siteurl==False:
        return 'http://www.google.com/search?q='+urllib2.quote(search)+'&oq='+urllib2.quote(search)
    else:
        return 'http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)+'&oq=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)

def getgooglelinks(search,siteurl=False):
   #google returns 403 without user agent
   headers = {'User-agent':'Mozilla/11.0'}
   req = urllib2.Request(getgoogleurl(search,siteurl),None,headers)
   site = urllib2.urlopen(req)
   data = site.read()
   site.close()

   #no beatifulsoup because google html is generated with javascript
   start = data.find('<div id="res">')
   end = data.find('<div id="foot">')
   if data[start:end]=='':
      #error, no links to find
      return False
   else:
      links =[]
      data = data[start:end]
      start = 0
      end = 0        
      while start>-1 and end>-1:
          #get only results of the provided site
          if siteurl==False:
            start = data.find('<a href="/url?q=')
          else:
            start = data.find('<a href="/url?q='+str(siteurl))
          data = data[start+len('<a href="/url?q='):]
          end = data.find('&amp;sa=U&amp;ei=')
          if start>-1 and end>-1: 
              link =  urllib2.unquote(data[0:end])
              data = data[end:len(data)]
              if link.find('http')==0:
                  links.append(link)
      return links

# Get the real webpage of the professor
def ReturnHomepage(links):
    
    education_links = []
    for link in links:
        if link.find(".edu") != -1:
            education_links.append(link)

    return education_links

def DownloadWebpage(edu_links,query):
    # This will download and write out the webpage of the dude we want
    low_length = 1000
    for link in edu_links:
        if len(link) < low_length:
            link_to_use = link
            low_length = len(link)
            
    # we will use the shortest link, which works because that will be the 
    # base url available
    req = urllib2.Request(link_to_use,None)
    resp = urllib2.urlopen(req)
    html_content = resp.read()
    
    # Now let's clean up these files
    soup = BeautifulSoup(html_content)
    text = soup.get_text()
    
    # Create filename to save the file
    print "Downloading: ", link_to_use
    filename = os.path.join("../","non_famous_websites",query + ".txt")
    with open(filename,'w') as f:
        f.write(text)
    
    return

if __name__ == "__main__":
    
    # Education links are good
    query = sys.argv[1]
    links = getgooglelinks(query)
    edu_links = ReturnHomepage(links)
    DownloadWebpage(edu_links,query)
    
    