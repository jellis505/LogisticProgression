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
    
    soup = BeautifulSoup(html_string)
    
    # Find the ingredients that are used
    ingredients_list = []
    lis = soup.find_all('li')
    for li in lis:
        if li.has_attr('itemprop'):
            if ul['itemprop'] == "ingredients":
                ingredients_list.append(li.string)
    
    # Now let's get the portions of the html page that correspond to the actual
    # instructions
    
    # find the div that holds the instuctions
    divs = soup.find_all('div')
    for div in divs:
        if div.has_attr('itemprop'):
            if div['itemprop'] == "recipeInstructions":
                instruction_div = div
                break
    
    # Now get all the p elements in the instruction div
    instruction_list = []
    p_elements = instruction_div.find_all('p')
    for p_element in p_elements:
        instruction_list.append(p_element.string)
    
    # Create strings out of the lists we have
    ingredients_string = ",".join(ingredients_list)
    instruction_string = " ".join(instruction_list)
            
    
    
    return ingredients_string,directions


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
    for file in html_files:
        with open(file,'r') as f:
            print "Processing file", file
            ingredients, directions = CleanHTML(f.read())
            raw_input("Press Enter")
    
    


