#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis and Jessica Ouyang
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web

import os, sys, shutil, getopt
from bs4 import BeautifulSoup
import urllib2

def GetURL(url_string,special):
    # This function returns the hmtl string from a url
    #INPUTS:
        #url_string = the address to be queried
        #special = a variable that will denote in the future if some special precautions must be taken
                    # to make the process work
    #OUTPUTS:
        #hmtl_string = the raw html string form the given url
    
    # The special variable will be used for sites like wikipedia that we need to spoof with some other tactic
    # to have access to the html page
    if special == None:
        req = urllib2.Request(url_string)
        response = urllib2.urlopen(req)
        html_string = response.read()
    return html_string

def GetRecipeURLs(html_string):
    # This function parses the webpage, and then finds all of the links to the recipes on the search page
    # INPUTS:
        # html_string = The html string from the foodnetwork.com search page
    # OUPUTS:
        # good_recipe_links = The links in list format to the recipes that could be extracted from the page
    
    # This is the domain name
    domain_name = "http://www.foodnetwork.com"
    
    # Create a beautiful soup object out of the html string
    recipe_links = []
    recipe_soup = BeautifulSoup(html_string)
    a_strings = recipe_soup.find_all('a')
    for a_string in a_strings:
        if a_string.has_attr('href'):
            recipe_links.append(a_string['href'])
    
    # Now clean the strings so that we only get the recipe strings
    good_recipe_links = []
    for recipe_link in recipe_links:
        if (recipe_link[0:8] == '/recipes') and ('/reviews/' not in recipe_link):
            good_recipe_links.append(domain_name + recipe_link)
    
    return good_recipe_links

def StoreHTMLPages(recipe_urls,folder_path):
    # This function outputs the urls to a specific directory
    # INPUTS:
        # recipe_urls = The recipes urls to be downloaded in list format
        # folder_path = the output directory to store the .html pages
    # OUTPUTS:
        # None
    
    for recipe_url in recipe_urls:
        new_html_string = GetURL(recipe_url,None)
        
        # Now fidn the name for the new_html_string
        last_slash = recipe_url.rfind('/');
        second_to_last_slash = recipe_url[0:last_slash-1].rfind('/')
        recipe_name = recipe_url[second_to_last_slash+1:last_slash] + ".html"
        
        # save the html string at this file
        output_file_name = os.path.join(folder_path,recipe_name)
        
        #Now output the html string
        with open(output_file_name, 'w') as f:
            f.write(new_html_string)
    
    return
        
    

if __name__ == "__main__":
    # This script takes a search page url, and finds all of the html recipes from food network for that person
    # The inputs are described below in the get-opt code, and usage is made very simple.
    # INPUTS:
        # search_name = the name used to search the food network, must be a famous chef
        # folder_path = the output directory to store the .html pages 
    #OUTPUTS: The output format is the downloaded .html pages in the directory specified as input
        # \folder_path
            # recipe1.html
            # recipe2.html
            # ...
            # recipe204.html
    
    
    ########### Command Line Inputs ########################
    # The variable names are here, and if they remain none then we need to exit
    search_name = None
    folder_path = None
    
    try:
        opts,args = getopt.getopt(sys.argv[1:],'i:n:h')
    except getopt.GetoptError:
        print "Usage Incorrect:"
        print "-i = The name of the person to be searched, should be in quotations"
        print "-n = The path to the folder where all of the files should be stored"
    
    for opt,arg in opts:
        if opt in ['-h']:
           print "GetChefPages = Downloads the pages of each chef based on a given search result"
           print "-i = The name of the person to be searched, should be in quotations"
           print "-n = The path to the folder where all of the files should be stored"
        elif opt in ['-i']:
            search_name = arg;
        elif opt in ['-n']:
            folder_path = arg
    
    # Check to make sure that we have the proper variables,
    # we need the search path and we need a place to download the files
    if (not search_name) or (not folder_path):
        print "Insufficient input: Please use -h for more information" 
        sys.exit(1)
        
    # Check to see if the folder path for the files exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    ############# Main Portion ################### 
    non_unique_urls = []
    for search_num in range(0,204,12):
        
        # We need to index how far into the search we travel on each page
        # Debug output to see how far we have made it in the link finding
        print "Finished recipes:", search_num

        # This must be addded on to the search page to move through the search results
        search_url = "http://www.foodnetwork.com/search/delegate.do?Nr=Record%20Type:Result&N=501%204294959872&fnSearchString="
        search_name = search_name.lower()
        
        # This url encodes the search name
        url_encoded_search_name = search_name.replace(" ", "%20")
        added_end_url = "&No=%d" % search_num
        
        # search_url must have the search name added on
        search_url = search_url + url_encoded_search_name
        
        # This function gets our html string
        print "Processing: ", search_url+added_end_url
        html_string = GetURL(search_url + added_end_url,None)
        # Returns the recipe webpages
        non_unique_urls.extend(GetRecipeURLs(html_string)) 

    # Now let's find the unique recipe urls
    unique_urls = []
    for non_unique_url in non_unique_urls:
        if non_unique_url not in unique_urls:
            unique_urls.append(non_unique_url)
    
    # Final Debug output
    print "The number of unique_urls found is:", len(unique_urls)
    
    # Now store the html pages in the proper directory
    StoreHTMLPages(unique_urls,folder_path)
    
        
    
