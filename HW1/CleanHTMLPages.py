#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis 
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web

import os,sys,shutil,getopt
from bs4 import BeautifulSoup

def CleanHTML(html_string):
    
    # This function returns the ingredients and directions for each Food Network recipe
    # The python parser for Python 2.7.2 can not process the foodnetwork pages, therefore,
    # you should install the lxml library for this code to work.
    soup = BeautifulSoup(html_string,"lxml")
    
    # Find the ingredients that are used
    ingredients_list = []
    lis = soup.find_all('li')
    for li in lis:
        if li.has_attr('itemprop'):
            if li['itemprop'] == "ingredients" and (li.string != None):
                ingredients_list.append(li.string.replace("\r",""))
    
    # Now let's get the portions of the html page that correspond to the actual
    # instructions
    
    # find the div that holds the instuctions
    instruction_div = None
    divs = soup.find_all('div')
    for div in divs:
        if div.has_attr('itemprop'):
            if div['itemprop'] == "recipeInstructions":
                instruction_div = div
                break
                
                
    # Now get all the p elements in the instruction div
    if instruction_div:
        instructions_text = instruction_div.get_text()
    else:
        instructions_text = ""
    
    """" This is slightly more complicated let's rely on the BeautifulSoup get_text function
         from the instruction div
    print instruction_div
    p_elements = instruction_div.find_all('p')
    for p_element in p_elements:
        print p_element
        print p_element.string
        print instruction_list
        instruction_list.append(p_element.string.replace("\r",""))
        raw_input("Waiting")
    """
    
    # Create strings out of the lists we have
    ingredients_string = ",".join(ingredients_list)
    instructions_text = instructions_text.replace('\n', ' ')
    instructions_string = instructions_text.replace('\r','')        
    
    
    return ingredients_string,instructions_string


if __name__ == "__main__":
    # This function takes each html file, and parses it and then finds
    # outputs the appropriate portions of each file to .html_cleaned
    
    # Input the directory that holds the author recipe folders
    top_level_dir = sys.argv[1]
    
    # Get the author directories from the high level dir
    author_dirs = [os.path.join(top_level_dir,o) for o in os.listdir(top_level_dir) if os.path.isdir(os.path.join(top_level_dir,o))]
    
    # Create a list of all of the html files from each directory
    html_files = []
    for author_dir in author_dirs: 
        html_files.extend([os.path.join(author_dir,o) for o in os.listdir(author_dir)])

    # Now clean each html file
    
    # This file will let us know if anything went wrong with any of the cleaning for the files
    bad_file = "bad_cleaning_record.txt"
    bad = open(bad_file,'w')
    
    for i,file in enumerate(html_files):
        
        if i % 10 == 0:
            print "Processing File Number", i
        
        with open(file,'r') as f:
            ingredients, directions = CleanHTML(f.read())
            
            if len(ingredients) > 0 and len(directions) > 0:
                with open(file.replace(".html",'.txt'),'w') as g:
                    g.write(ingredients)
                    g.write('\n')
                    g.write(directions)
            else:
                bad.write(file + '\n')




