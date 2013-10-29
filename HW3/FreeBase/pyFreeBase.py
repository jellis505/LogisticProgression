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
        
        # Finds the API key within the directory structure
        if os.path.exists("Api_Key.txt"):
            api_key_path = "Api_Key.txt"
        elif os.path.exists("FreeBase/Api_Key.txt"):
            api_key_path = "FreeBase/Api_Key.txt"
        else:
            print "CAN'T FIND PATH TO API KEY, PLEASE INSERT IT MANUALLY INTO THE __INIT__ FUNCTION OF pyFreeBase.py"
            sys.exit(0)
        
        
        self.api_key = open(api_key_path).read()
        self.service_url = 'https://www.googleapis.com/freebase/v1/search'
        self.mqlread_url = "https://www.googleapis.com/freebase/v1/mqlread" 
        
    def GetQuery(self,query):
        # Set up the parameters for the query
        params = {
            'query' : query,
            'type' : '/people/person',
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
        no_birthday = False
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
            birth_string = result["date_of_birth"][0]
            find_T = birth_string.find("T")
            
            # This finds if we can't find the birthday
            if len(birth_string) < 0:
                no_birthday = True
                break
            # This removes if for some reason the person has a string denoting the exact time of 
            # birth in the name
            if find_T != -1:
                birth_string = birth_string[0:find_T]
            
            # Now get the year month and date
            parts = birth_string.split("-")
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
        
        if no_birthday:
            # If we don't find the birthday, just take a guess
            day = 01
            month = 01
            year = 1900
        
        # Debug print output
        print "The Birthday of %s is year=%d, month=%d, day=%d" % (query_id["id"],year,month,day)
        
        return month,day,year
        
        
if __name__ == "__main__":
    # Let's run some tests
    query = sys.argv[1]
    free_base = FreeBase()
    result = free_base.GetQuery(query) 
    month, day, year = free_base.GetBirthday(result)