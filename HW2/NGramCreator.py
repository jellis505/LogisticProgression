#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# News Rover System
# Digital Video & Multimedia Lab
# Columbia University

import os, sys, shutil
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ingrams
import math
from nltk.model.ngram import NgramModel


class NGramModel():
    """This class creates an Ngram from a given amount of text"""
    
    """ Big Scale Functions"""
    def __init__(self,N,back_off_params=None):
        # Description = This intilializes the class that we have that is used for creation of the N-Gram language model
        # Inputs:
            # N = The N for our N-Gram model
            # back_off_params = The parameters used in back_off 
        # Outputs:
            # None
            
        #This sets up our NGram Creator
        self.N = N
        self.use_sentences = True
        # Set these to true if we want to use padding on either side for creation of our n-grams
        self.leftpad = False
        self.rightpad = False
        self.back_off_params = back_off_params
        
        return
    
    def GetTokenizedSentences(self,file):
        # Description = Take a file and gets the tokenized sentences
        # Inputs:
            # file = Raw text file to be used for language modeling
        # Outputs:
            # tokenized_sentences = A list of all of the content in the file seperated by sentences.

       # This function simply turns all of the work into a really long vector of ngrams
        
        # This file runs the creation of the n-gram
        # Read in the file
        with open(file,"r") as f:
            content_string = f.read()
        
        # Get the tokenized files
        tokenized_sentences = self.Tokenize_File(content_string)
        return tokenized_sentences
    
    def TrainNGramModel(self,file,modelfile=None,output_file=False):
        # Description = Wrapper function that takes in a plain text file and then outputs the modelfile
        # Inputs:
            # file = The raw text file
            # modelfile = The output file that model will be output to
            # output_file = If this is True we do output the model
        # Outputs:
            # output = A tuple with the list of grams and the list of counts of those grams

       # This function simply turns all of the work into a really long vector of ngrams
        
        # This file runs the creation of the n-gram
        # Read in the file
        with open(file,"r") as f:
            content_string = f.read().lower()
        
        # Get the tokenized files
        tokenized_sentences = self.Tokenize_File(content_string)
        
        # Get the NGrams
        n_grams = self.GetNGrams(tokenized_sentences)
        
        # Now create the n_gram representation
        ngram_model = self.CreateNGramVec(n_grams)
        
        # Output the model
        if output_file:
            self.OutputNGrams(modelfile,ngram_model)
    
        return ([ a for a,b in ngram_model ], [ b for a,b in ngram_model ])
    
    def GetTestPerplexity(self,test_file,model_file, use_backoff=False,smoothing=None):
        # Description = Get the Test Perplexity of a given test text set based on a pre-trained model.  
                        # This function has no outputs, all of the necessary outputs are output to standard output.
        # Inputs:
            # test_file = The path to the raw text file to be used
            # model_file = The name without extension of the model that is going to be used.
                            # The function will look for this model file in models
            #use_backoff = this should be true if backoff is used
            # smoothin = This is True if smoothing is used, False if not
        # Outputs:
            # entropy_average = returns the average entropy per n-gram = totalentropy/n_grams
            # seen_entropy_average = the average entropy on only the seen n-grams we had in our model
            # prob_vec = A vector that holds the probability of each n_gram, multiplied by the count of that n_gram.
                        # Used for the interpolation
            # total_count = The number of total non-unique n-grams modeled.
            
       # This function simply turns all of the work into a really long vector of ngrams
        
        # This reads in the trained model files and the new data, and compares the perplexity
        # Let's read in the ngram models that we will need
        
        # Let's see what type of smoothing we can use
        prob_vec = []
        self.smoothing = smoothing
        self.V = []
        ngram_models = []
        for i in range(1,self.N+1):
            train_model_file ="models/" + model_file + "_" + str(i) + ".model"
            ngrams,counts = self.ReadModelFile(train_model_file)
            total_grams = 0
            for count in counts:
                total_grams += count
            # Store the model in a vector
            ngram_models.append((ngrams,counts,total_grams))
            self.V.append(float(len(ngram_models[0][1])))
        # Now let's get our V value for smoothing
        
        print len(ngram_models)
        # Let's make this a class variable to make everything easier
        self.ngram_models = ngram_models
        test_grams,test_counts = self.TrainNGramModel(test_file)
        print "Got the test values"
        print len(test_grams)
        # Now we have the model to be tested, and our trained model
        total_count = 0
        total_seen_count = 0
        total_perplexity = 0
        entropy_vec = []
        seen_entropy_vec = []
        unseen_count = 0
        for i,(gram,count) in enumerate(zip(test_grams,test_counts)):
            #if not i % 1000:
            #    print "Finished %d of %d test samples" % (i,len(test_counts))
            total_count += count
            if not use_backoff:
                entropy,unseen,prob = self.GetEntropyofGram(gram)
                prob_vec.append(prob)
                # This does it for everything
                entropy_vec.append(count*entropy)
            else:
                entropy,unseen,prob = self.GetEntropyofGram_Backoff(gram)
                prob_vec.append(prob)
                # This does it for everything
                entropy_vec.append(count*entropy)
            if not unseen:
                total_seen_count += count
                seen_entropy_vec.append(count*entropy)
            else:
                 unseen_count += count*unseen
            
                
            
        # Output to screen what for pre-backoff tests
        if not self.back_off_params:
            print "The total entropy of the test text for n=%d is: %f" % (self.N,sum(entropy_vec))
            print "These are the total number of percentage of unseen grams form seen gram:", unseen_count/(float(total_count))
            print "The total seen entropy of the test text for n=%d is: %f" % (self.N,sum(seen_entropy_vec)/float(total_seen_count))
            print "The total entropy of the test text for n=%d is: %f" % (self.N,sum(entropy_vec)/float(total_count))
            print "Total Seen =", total_seen_count
            print "Total Elements=", total_count
        # Output to screen for each back off parameter
        else:
            print "The total entropy of for lambda =", self.back_off_params
            print "Total Entropy = ", sum(entropy_vec)
            print "Average Entropy =", sum(entropy_vec)/float(total_count)
            print "Seen Entropy =", sum(seen_entropy_vec)/float(total_seen_count)
            print "Total Seen =", total_seen_count
            print "Total Elements=", total_count
        return sum(entropy_vec)/float(total_count),sum(seen_entropy_vec)/float(total_seen_count), prob_vec, total_count
    
    
    """ Utility Functions"""
    def Tokenize_File(self,content_string):
        # Description = This function tokenizes a raw text file into a list of sentences
        # Inputs:
            # content_string = The raw string content for the given file
        # Outputs:
            # n_grams = This is the raw_string content seperated into different sentences,
                #based on the punkt nltk tokenizer

       # This function simply turns all of the work into a really long vector of ngrams
        
        # This section used the built in nltk tokenizer, which works on sentences at a time.
        # So in our language model we will only take into account sentences
        if self.use_sentences:
            sentences = sent_tokenize(content_string)
            tokenized_vec = []
            for sentence in sentences:
                # let's tokenize the words
                tokens = word_tokenize(sentence)
                tokenized_vec.append(tokens)
        return tokenized_vec
    
    def GetNGrams(self,tokenized_sentences):
        # Description = Takes the tokenized sentences and outputs all of the n-grams from a given text
        # Inputs:
            # Tokenized Sentences = The sentences after we tokenize the file to be used.
        # Outputs:
            # n_grams = The list of n_grams found in the file, not unique

       # This function simply turns all of the work into a really long vector of ngrams
        n_grams = []
        for token_sent in tokenized_sentences:
            sent_n_grams = ingrams(token_sent,self.N,self.leftpad,self.rightpad)
            n_grams.extend(sent_n_grams)
        
        return n_grams
    
    def CreateNGramVec(self,n_grams):
        # Description = Given all the n-grams in a text, this functions creates a vector of unique n,grams and their counts
        # Inputs:
            # n_grams = The n_grams for a given text
        # Outputs:
            # output = tuple of two lists, list 1 is the unique grams and list 2 is the
            # count that each gram appeared in this data
        
        # This function creates the representation for our text
        unique_n_grams = []
        n_gram_count = []
        for i,n_gram in enumerate(n_grams):
            
            # For Debug Output
            #if not i % 10000:
            #    print "Processed: %d of %d\r" % (i,len(n_grams))
            
            if n_gram in unique_n_grams:
                index = unique_n_grams.index(n_gram)
                n_gram_count[index] += 1
            else:
                unique_n_grams.append(n_gram)
                n_gram_count.append(1)
        
        #print "The Length of our n_grams is:", len(unique_n_grams)
        #print len(n_gram_count)
        return zip(unique_n_grams, n_gram_count)
        
    def OutputNGrams(self,modelfile,output_data):
        # Description = This function outputs the grams and counts for an n-gram model to the specified file
        # Inputs:
            # modelfile = The file to output the model too
            # output_data = The data, grams and counts to be output too
        # Outputs:
            # None
        
        
        # Output the model file
        # it would be easier to pickle these, but then people can't look at the data
        # unless they know what they are doing which could be annoying
        print "Ouputtting Model to file", modelfile
        with open(model_file, "w") as f:
            for gram,val in output_data:
                f.write("'''''".join(gram))
                f.write("\t")
                f.write(str(val))
                f.write("\n")
    
    def ReadModelFile(self,modelfile):
        # Description = Reads in the grams and counts to variables for a particular n-gram model
        # Inputs:
            # modelfile = The model to be read into a list structure
        # Outputs:
            # grams = A list of list of the grams present
            # counts = A list of the counts for each gram
        
        with open(modelfile,"r") as f:
            l = f.readlines()
            lines = [line.rstrip("\n") for line in l]
            grams = []
            counts = []
            for line in lines:
                parts = line.split("\t")
                gram = tuple(parts[0].split("'''''"))
                count = int(parts[1])
                grams.append(gram)
                counts.append(count)
        return grams,counts
    
    def GetEntropyofGram_Backoff(self,gram):
        # Description = This function returns the entropy of a given gram using the back-off parameter
        # Inputs:
            # gram = The n-gram in tuple form
        # Outputs:
            # entropy = the entropy of the given gram for the trained model 
            # total_prob = The probabliltiy of the given gram given back off
            # unseen = Whether the gram was seen or unseen
        
        
        # This will calculate our grams
        prob_vec = []
        unseen = 0
        for i in range(0,len(gram)):
            # Find the gram
            a = tuple(gram[0:i+1])
            if i > 0:
                b = tuple(gram[0:i])
                
            gram_exists = True
            #if len(a) == 1:
            #    a = a[0]
            #else:
            #    a = tuple(a)
            
            # Find the new gram in the index
            # If the gram is brand new we don't want it to kill our program, so we catch an error
            # if the value is not in the index
            try:
                if i == 0:    
                    gram_num = self.ngram_models[i][0].index(a)
                else:
                    gram_num = self.ngram_models[i][0].index(a)
                    gram_num_b = self.ngram_models[i-1][0].index(b)
            except:
                gram_exists = False

            # Only calculate the probability if the value exists
            if gram_exists and i == 0:    
                prob = (self.ngram_models[i][1][gram_num] + 1)/float(self.ngram_models[i][2] + self.V[i])
                prob_vec.append(prob)
                
            elif gram_exists:
                prob =  (self.ngram_models[i][1][gram_num] + 1)/float(self.ngram_models[i-1][1][gram_num_b] + self.V[i])
                prob_vec.append(prob)
            else:
                unseen = 1
                prob_vec.append((1/self.V[i]))
        
        # Now this is where we multiply by our parameters for back off
        total_prob = prob_vec[0]*self.back_off_params[0] + prob_vec[1]*self.back_off_params[1] + prob_vec[2]*self.back_off_params[2]
        entropy = total_prob*math.log(total_prob)
        return entropy, unseen, total_prob
    
    def GetEntropyofGram(self,gram):
        # Description = This function returns the entropy of a given gram with the used language model
        # Inputs:
            # gram = The n-gram in tuple form
        # Outputs:
            # entropy = the entropy of the given gram for the trained model 
            # prob = The probabliltiy of the given gram
            # unseen = Whether the gram was seen or unseen
        
        
        # This will calculate our grams
        a = tuple(gram)
        gram_exists = True
        unseen = 0;
        # Try to find the correct gram count, if this gram does not exist then we won't 
        # try to access it's counts
        try:
            gram_num = self.ngram_models[self.N-1][0].index(a)
        except:
            gram_exists = False
        
        
        # Get the entropy with Laplace smoothing
        if self.smoothing:
            # Now let's get the entropy with Laplace smoothing
            # This is (N(w) + 1)/(N + V)
            if gram_exists:
                prob = (self.ngram_models[self.N-1][1][gram_num] + 1) /float(self.ngram_models[self.N-1][2] + self.V[self.N-1])
                entropy = prob*math.log(prob)
            else:
                unseen = 1
                entropy = (1/self.V[self.N-1])*math.log(1/self.V[self.N-1])
                prob = 1/self.V[self.N-1]
        else:
            
            # This is N(w)/N
            #Now get the entropy
            if gram_exists:
                prob = self.ngram_models[self.N-1][1][gram_num]/float(self.ngram_models[self.N-1][2])
                entropy = prob*math.log(prob)
            else:
                unseen = 1
                entropy = 0
                prob = 0

        return entropy, unseen,prob
        
if __name__ == "__main__":
    
    # This runs tests for this functiontionality
    """Training Script"""
    """
    for N in range(1,7):
        train_file = "data/TheScarletLetter_train.txt"
        model_file = "models/TheScarletLetter_" + str(N) +".model"
        ngrammer = NGramModel(N)
        ngrammer.TrainNGramModel(train_file,model_file,True)
    quit()
    """
    
    """Testing Script"""
    """
    for N in range(1,7):
        train_file = "data/TheScarletLetter_train.txt"
        test_file = "data/TheScarletLetter_dev.txt"
        ngrammer = NGramModel(N)
        train_sents = ngrammer.GetTokenizedSentences(train_file)
        test_sents = ngrammer.GetTokenizedSentences(test_file)
        test_words = []
        for sent in test_sents:
            test_words.extend(sent)
             
        # Train the model then test it
        ngram_model = NgramModel(N,train_sents,False,False)
        entropy = ngram_model.entropy(test_words)    
        print "For %d: the perplexity is:", entropy
    quit()   
    """
    """ This is to test the best N"""
    """
    for N in range(1,7):
        test_file = "data/TheScarletLetter_dev.txt"
        ngrammer = NGramModel(N)
        ngrammer.GetTestPerplexity(test_file, False, True)
    quit()
    """
    """ This is to test the best lambdas that we have here"""
    lambdas = [[0.0,0.5,0.5],[0.33,0.33,0.33],[0.2,0.4,0.4],[0.5,0.25,0.25],[0.25,0.5,0.25],[0.25,0.25,0.5],[0.1,0.2,0.7]]
    for back_off in lambdas:
        N = 3
        test_file = "data/ATaleofTwoCities_dev.txt"
        ngrammer = NGramModel(N,back_off)
        ngrammer.GetTestPerplexity(test_file,"ATaleofTwoCities", True, True)
                
        
    
    