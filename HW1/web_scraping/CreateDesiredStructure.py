#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis and Jessica Ouyang
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web


import os, sys, shutil
import random


def ReplaceExt(file,ext):
    last_dot = file.rfind('.')
    return file[0:last_dot] + ext

def GetFilesNotInBadFile(top_level_dir,bad_file):
    
    # This get the files we don't want to use for some reason, because the parsing wasn't great
    bad_files = []
    with open(bad_file,"r") as f:
         lines = f.readlines()
         bad_files = [line.rstrip("\n") for line in lines]
    
    # Get the author directories from the high level dir
    author_dirs = [os.path.join(top_level_dir,o) for o in os.listdir(top_level_dir) if os.path.isdir(os.path.join(top_level_dir,o))]
    
    # Create a list of all of the html files from each directory
    # sorted into different lists, so that we have some from each
    html_files = []
    html_files_fullpath = []
    for author_dir in author_dirs: 
        html_files.append([o for o in os.listdir(author_dir) if ".html" in o])
        html_files_fullpath.append([os.path.join(author_dir,o) for o in os.listdir(author_dir) if ".html" in o])
    
    # Get all of the text files
    txt_files = []
    for html_file_list in html_files:
        author_txt_files = []
        for html_file in html_file_list:
            author_txt_files.append(ReplaceExt(html_file,".txt"))
        txt_files.append(author_txt_files)
    
    # Now we have all of the text files, and the test files
    # Let's randomly choose what are going to be train and test sets
    
    return html_files,txt_files,author_dirs
    
def CreateTrainandTest(html_files,txt_files,author_dirs,bad_file):
    # This createst the train and test split
    
    # This get the files we don't want to use for some reason, because the parsing wasn't great
    bad_files = []
    with open(bad_file,"r") as f:
         lines = f.readlines()
    for line in lines:
        last_slash = line.rfind("/")
        bad_files.append(ReplaceExt(line[last_slash+1:],""))
    
    
    # Let's make the train and test splits for each author.
    # tuples holding file, and then also the author for each file
    train_files = []
    test_files = []
    for author_dir,html_file_list,txt_file_list in zip(author_dirs,html_files,txt_files):
        # Get the author name
        last_slash = author_dir[:-1].rfind("/")
        is_last_char_slash = author_dir[-1] == "/"
        if is_last_char_slash:
            author_name = author_dir[last_slash+1:-1]
        else:
            author_name = author_dir[last_slash+1:]
    
        # Kill the extension on the files
        html_file_no_ext = [ReplaceExt(o,"") for o in html_file_list]
        html_file_no_ext = [o for o in html_file_no_ext if o not in bad_files]
        
        # shuffle the files so that we get a random mix for train and test
        random.shuffle(html_file_no_ext)
        train_for_author = html_file_no_ext[0:100]
        test_for_author = html_file_no_ext[101:151]
        
        for file in train_for_author:
            train_files.append((file,author_name))
        for file in test_for_author:
            test_files.append((file,author_name))
    
    return train_files, test_files

if __name__ == "__main__":
    """ This script takes the desired directory that we have all of the files in by author, 
    chooses the test files, and then moves over them to the directory structure as discussed in the 
    report as the desired format
    """
    
    #INPUTS:
        # top_level_dir = the directory that contains the folder with each authors recipes
    #OUTPUTS:
        # ../train_labels.txt = The training file in the desired format as described in the HW write-up
        # ../test_labels.txt = The Testing file in the desired format as described in the HW write-up
        # data/ = The flat directory with each of the .html and .txt files that were created using 
            # GetChefPages.py and CleanHTMLPages.py
    
    #########Get the Files that we want##############
    # Input the directory that holds the author recipe folders
    top_level_dir = sys.argv[1]
    bad_file = "bad_cleaning_record.txt"
    
    # Create the txt files from the html files
    html_files,txt_files,author_dirs = GetFilesNotInBadFile(top_level_dir,bad_file)
    
    # Create the train and test tuples
    train_files,test_files = CreateTrainandTest(html_files,txt_files,author_dirs,bad_file)
    
    # Output the train and test_files to the head directory
    with open("../train_labels.txt","w") as f:
        for train_file in train_files:
            f.write(train_file[0])
            f.write(",")
            f.write(train_file[1])
            f.write("\n")
    
    with open("../test_labels.txt","w") as f:
        for test_file in test_files:
            f.write(test_file[0])
            f.write(",")
            f.write(test_file[1])
            f.write("\n")
    
    
    
    