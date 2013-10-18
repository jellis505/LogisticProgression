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



""" This class uses an already created dictionary, and performs feature extraction from"""
class FeatureExtractor:
    # This class performs feature extraction 
    
    def __init__(feature_type,dict_file,idf_file):
        
        #Give the feature extractor the file, and 
        self.feature_type = feature_type
        self.dict_file = dict_file
        # Load the dictionary that is used for each word
        self.word_dict = self.LoadWordDict(self.dict_file)
        self.IDF = self.LoadWordIDF(self.idf_file)
        return None
    
    # This function loads the word dictionary 
    def LoadWordDict(dict_file):
        words = []
        with open(dict_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.split(",")
                words.append(parts[0])                
        return words
    
    def LoadWordIDF(IDF_File):
        IDF = [];
        with open(IDF_File,'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip("\r\n")
                line = line.rstrip("\n")
                parts = line.split(",")
                IDF.append(float(parts[1]))
        return IDF
    
    def CreateTermVector(plain_text_file):
        with open(plain_text_file,'r') as f:
            
            # Get the cleaned words
            cleaned_words =  self.GetCleanWords(f.read())
            
            # Create the term vector of all zeros
            term_vec = [0 for word in words]
            
            for word in cleaned_words:
                index = self.word_dict.index(word)
                term_vec[index] += 1
        
        return term_vec
        
    def CreateBoW(plain_text_file):
            with open(plain_text_file,'r') as f:
            
            # Get the cleaned words
            cleaned_words =  self.GetCleanWords(f.read())
            
            # Create the term vector of all zeros
            BoW = [0 for word in words]
            
            for word in cleaned_words:
                index = self.word_dict.index(word)
                BoW[index] = 0; 
        
        return BoW
    
    def NormalizebyIDF(tf,idf):
        """The input values should be np.arrays of the same length"""
        if type(tf) is list:
            tf = np.array(tf)
        if type(idf) is list:
            idf = np.array(idf)
        return TF_IDF = np.multiply(a,b)

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
    
if __name__ == "__main__":
    # This function runs some command line procedure, but this class will probably be called from 
    # some other script that is created.
    
    
    
    
        
    