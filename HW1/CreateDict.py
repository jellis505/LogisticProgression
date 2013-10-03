#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis 
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web

import os,sys,shutil,getopt
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.corpus import stopwords

#Global Variable -- List of english stopwords
stopwords_list = stopwords.words('english')

def GetCleanWords(content_string):
    
    # Tokenize the sentences using hte Punkt word Tokenizer
    tokenized_words = PunktWordTokenizer().tokenize(content_string)
    
    #Now let's remove the stop words
    tokenized_words = [word for word in tokenized_words if word.lower() not in stopwords_list]
    
    # Now let's remove all of the solely punctuation.
    punctuation_list = ['.',',',';',':','!','?']
    tokenized_words = [word for word in tokenized_words if word not in punctuation_list]
    
    # Finally let's get rid of the punctuation at the end of each word
    cleaned_words = []
    for word in tokenized_words:
        if word[-1] in punctuation_list:
            cleaned_words.append(word[:-1])
        else:
            cleaned_words.append(word)

    return cleaned_words

def UpdateDict(words,counts,cleaned_words):
    # This function updates out words and counts
    for clean_word in cleaned_words:
        if clean_word in words:
            word_index = words.index(clean_word)
            counts[word_index] += 1
        else:
            words.append(clean_word)
            counts.append(1)
    
    return words, counts
    
def CreateWordsandCountsFile(txt_files,word_count_file):
    # This function creates the dircitonary file
    ######## Dictionary Creation ################
    words = []
    counts = []
    for file in txt_files:
        with open(file,'r') as f:
            # Return the cleaned text and words
            cleaned_words = GetCleanWords(f.read())
            words,counts = UpdateDict(words,counts,cleaned_words)
    
    # Output Debug these lengths should be the same
    print "The length of our word vector is: ", len(words)
    print "The length of our counts vector is: ", len(counts)
    
    # Output to a file
    with open(word_count_file,'w') as f:
        for word,count in zip(words,counts):
            f.write(word)
            f.write(",")
            f.write(str(count))
            f.write("\n")
    
    return words,counts

if __name__ == "__main__":
    # This function creates a dictionary across the words that are found in each recipe
    
    ##########Get list of all files##################
    # Input the directory that holds the author recipe folders
    top_level_dir = sys.argv[1]
    
    # Get the author directories from the high level dir
    author_dirs = [os.path.join(top_level_dir,o) for o in os.listdir(top_level_dir) if os.path.isdir(os.path.join(top_level_dir,o))]
    
    # Create a list of all of the html files from each directory
    txt_files = []
    for author_dir in author_dirs: 
        txt_files.extend([os.path.join(author_dir,o) for o in os.listdir(author_dir) if ".txt" in o])
    
    # Name of the output file
    outputfile = "wordcount.csv"
    wrods,counts = CreateWordsandCountsFile(txt_files,outputfile)
    
            
                        
    
    