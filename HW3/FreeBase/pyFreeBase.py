#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis and Jessica Ouyang
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web

import sys, getopt, os
import urllib2, urllib
import json

# This code example is based off of google api documentation
# https://developers.google.com/freebase/v1/search-overview

class FreeBase():
    def __init__(self):
        # This is the init function for freebase
        self.api_key = open("Api_key.txt").read()
        self.service_url = 'https://www.googleapis.com/freebase/v1/search'
        self.mqlread_url = "https://www.googleapis.com/freebase/v1/mqlread" 
        
    def GetQuery(self,query):
        # Set up the parameters for the query
        params = {
            'query' : query,
            'key' : self.api_key
        }
        
        # Create the query url
        query_url = self.service_url + "?" + urllib.urlencode(params)
        print query_url
        response_dict = json.loads(urllib2.urlopen(query_url).read())
        
        # Now let's print the scores for debug
        #### Debug
        #for result in response_dict['result']:
        #    print result['name'] + " (" + str(result["score"]) + ")"
        
        # Grab the run with the closest name
        correct_result = None
        for result in response_dict['result']:
            if result['name'].lower() == query.lower():
                correct_result = result
                print "The correct name was found and is: ", result['name'].lower()
                break
        
        # Check to make sure that we found the name
        if not correct_result:
            correct_result = response_dict['result'][0]
            
        return correct_result 
    
    def GetBirthday(self,query_id):
        # Now let's get the birthday for the people
        query = [{'id': query_id["id"], 'type': '/people/person', "date_of_birth" : []}]
        params = {
            "query" : json.dumps(query),
            "key" : self.api_key
        }
        
        # Create the query url for birthday
        query_url = self.mqlread_url + "?" + urllib.urlencode(params)
        response_dict = json.loads(urllib2.urlopen(query_url).read())
        
        # Now extract the birthday
        for result in response_dict['result']:
            parts = result["date_of_birth"][0].split("-")
            year = parts[0]
            month = parts[1]
            day = parts[2]
        
        # Debug print output
        print "The Birthday of %s is year=%s, month=%s, day=%s" % (query_id["id"],year,month,day)
        
        return month,day,year
        
        
if __name__ == "__main__":
    # Let's run some tests
    query = sys.argv[1]
    free_base = FreeBase()
    result = free_base.GetQuery(query) 
    month, day, year = free_base.GetBirthday(result)