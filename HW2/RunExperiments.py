#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# News Rover System
# Digital Video & Multimedia Lab
# Columbia University

import os, sys, getopt
from NGramCreator import NGramModel


def ReplaceExt(srcname, newext):
    filename, fileext = os.path.splitext(srcname)
    return filename + newext

def GetonlyFileName(srcname):
    filename, fileext = os.path.splitext(srcname)
    last_slash = filename.rfind("/")
    return filename[last_slash+1:]


if __name__ == "__main__":
    
    # Now let's take the arguments and see what happens
    try:
        opts, args = getopt.getopt(sys.argv[1:],'m:b:hn:t:l:')
    except getopt.GetoptError:
        print "Usage Error: Please see help"
        sys.exit(1)
    
    
    back_off_params = None
    trainmodel = None
    N = None
    test_file = None
    trainmodels = None
    for opt,arg in opts:
        if opt in ['-m']:
            trainmodel = arg
        elif opt in ['-b']:
            back_off_params = [float(a) for a in arg.split(",")]
        elif opt in ['-h']:
            print "Help"
            print "n: the N gram model used"
            print "b: The back off parameters if we wanna use back_off"
            print "t: The test textfile"
            print "m: the name of the training models to be used in the model directory"
        elif opt in ['-n']:
            N = int(arg)
        elif opt in ['-t']:
            test_file = arg
        elif opt in ['-l']:
            interp_params = [float(a) for a in arg.split(",")]
    
    # Output what we will do
    print "The training model is: ", trainmodel
    print "The number of N is: ", N
    print "The file to be tested is: ", test_file
    
    # This sets up the variables in case we want to do an interpolation
    if trainmodel.find(",") != -1:
        trainmodels = trainmodel.split(".,")

    # Check to make sure we have all the variables
    if not(trainmodel and N and test_file):
        print "Need more parameters, please use -h for instructions"
        sys.exit(1)
    
    if not trainmodels:
        # This is the portion that actually runs the experiments using the given parameters
        n_grammer = NGramModel(N,back_off_params)
        entropy1,entropy_seen1 = n_grammer.GetTestPerplexity(test_file,trainmodel,True,True)
    
    else:
        n_grammer = NGramModel(N,back_off_params)
        entropy2,entropy_seen2 = n_grammer.GetTestPerplexity(test_file,trainmodels[1],True,True)
        entropy1,entropy_seen1 = n_grammer.GetTestPerplexity_2models(test_file,trainmodels[0],True,True)
        # Combine the two outputs using the 
        ave_entropy_interp = entropy2
        
        print "The Average Entropy of an interpolated model is: "
        print "The interpolation parameters are: ", interp_params
    
    
            
        