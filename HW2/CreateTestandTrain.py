#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# News Rover System
# Digital Video & Multimedia Lab
# Columbia University


import os, sys, shutil
import nltk
from math import floor


# Simple Utility functions, they do what their name says
def ReplaceExt(srcname, newext):
    filename, fileext = os.path.splitext(srcname)
    return filename + newext

def GetOnlyFileName(srcname):
    filename, fileext = os.path.splitext(srcname)
    last_slash = filename.rfind("/")
    return filename[last_slash+1:]

if __name__ == "__main__":
    
    
    #######File Description############
    # Description: This function splits the data into train,dev,and test
    # Inputs:
        # file = The file that will be split
    # Outputs:
        # trainfile = data/<file>_train.txt and contains 60% of the original file
        # testfile = data/<file>_test.txt and contains 20% of the original file
        # devfile = data/<file>_dev.txt and contains 20% of the original file
        
        
    # This function seperates the train and test_splits
    
    full_file = sys.argv[1]
    with open(full_file,'r') as f:
        full_text = f.read()
    
    # Let's use 20% for deva nd 20% for test
    full_len = len(full_text)
    
    # We need at least 100,000 words in this data set.
    # Al tale of two Cities has 135,420 words
    #http://indefeasible.wordpress.com/2008/05/03/great-novels-and-word-count/
    
    # Get the right names to output
    filename = GetOnlyFileName(full_file)
    trainfile = "data/" + filename + "_train.txt"
    devfile = "data/" + filename + "_dev.txt"
    testfile = "data/" + filename + "_test.txt"
    
    with open(trainfile,'w') as f:
        first_part_last_dot = full_text[0:int(floor(full_len*0.6))].rfind(".")
        f.write(full_text[:first_part_last_dot])
    
    with open(devfile,'w') as f:
        second_part_last_dot = first_part_last_dot + 1 + full_text[first_part_last_dot+1:first_part_last_dot+int(floor(full_len*0.2))].rfind(".")
        f.write(full_text[first_part_last_dot+1:second_part_last_dot])
    
    with open(testfile,"w") as f:
        third_part_last_dot = second_part_last_dot + 1 + full_text[second_part_last_dot+1:].rfind(".")
        f.write(full_text[second_part_last_dot+1:third_part_last_dot])
    
    
    
    