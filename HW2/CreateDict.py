#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis 
# DVMM Lab Columbia University

import os,sys,shutil,getopt
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import math


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
    
    # Now let's stem each of the words to lower our word count
    wnl = WordNetLemmatizer()
    clean_and_stemmed_words = [wnl.lemmatize(cleaned_word) for cleaned_word in cleaned_words] 
    
    return clean_and_stemmed_words

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

def CreateIDFScores(words,words_in_files):
    """ This function creates the idf scores for each of the 
    words in our dictionary"""
    
    IDF_denom = [0 for word in words]
    for i,word in enumerate(words):
        for words_in_file in words_in_files:
            if word in words_in_file:
                IDF_denom[i] = IDF_denom[i]+1
    
    # Now let's create the true IDF value,
    # which is ln(num_of_doc/(IDF_Denom))
    num_of_doc = len(words_in_files)
    IDF_Score = [math.log(num_of_doc/idf_d) for idf_d in IDF_denom] 
    
    return IDF_Score
    
    
def CreateDictFile(txt_files,word_count_file):
    # This function creates the dircitonary file
    ######## Dictionary Creation ################
    words = []
    counts = []
    words_in_files = []
    for file in txt_files:
        with open(file,'r') as f:
            # Return the cleaned text and words
            cleaned_words = GetCleanWords(f.read())
            words_in_files.append(cleaned_words)
            words,counts = UpdateDict(words,counts,cleaned_words)
    
    # Output Debug these lengths should be the same
    print "The length of our word vector is: ", len(words)
    print "The length of our counts vector is: ", len(counts)
    IDF = CreateIDFScores(words,words_in_files);
    
    return words,counts,IDF
 

if __name__ == "__main__":
    # This function creates a dictionary across the words that are found in each recipe
    
    ##########Get list of all files##################
    # Input the directory that holds the author recipe folders
    top_level_dir = sys.argv[1]
    dict_file = sys.argv[2]
    
    
    
    # Get the author directories from the high level dir
    author_dirs = [os.path.join(top_level_dir,o) for o in os.listdir(top_level_dir) if os.path.isdir(os.path.join(top_level_dir,o))]
    
    # Create a list of all of the html files from each directory
    txt_files = []
    for author_dir in author_dirs: 
        txt_files.extend([os.path.join(author_dir,o) for o in os.listdir(author_dir) if ".txt" in o])
    
    # Name of the output file
    words,counts,IDF = CreateDictFile(txt_files,outputfile)
    
    # Now output the files to the desired directories
    # file paths
    with open("wordcount.csv",'w') as f:
        for word,count in zip(words,counts):
            f.write(word)
            f.write(",")
            f.write(str(count))
            f.write("\n")
    
    with open("IDF_Scores.csv","w") as f:
        for word,idf in zip(words,IDF):
            f.write(word)
            f.write(",")
            f.write(str(idf))
            f.write("\n")
    
    print "Finished Dictionary Creation"
    
    
    
    
            
                        
    
    