#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis 
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web

import os,sys,shutil
import numpy as np
from scipy.optimize import f_min_l_bfgs_b
import random
import sklearn

# We will use the logistic function in our autoencoder
def logistic(x):
    return 1/(1+np.exp(-x))

def der_logistic(x):
    return x*(1-x)

class AutoEncoder:
    """ This class creates an autoencoder object, and then returns the learned matrix function"""
    
    def __init__(self, feature_length, num_hidden):
        # This function will initialize the values that we want in our function for the matrix
        self.feature_length = feature_length
        self.num_hidden = num_hidden
        self.alpha = 3e-3
        self.learning_rate = .001
        self.max_iter = 200
        
        # This section initializes the weight matrices that we will need for the autoencoder
        # We have two different layers the layer into the hidden layer, and also the output
        self.w_hidden = np.random.uniform(-1,1,(num_hidden,feature_length))
        self.w_output = np.random.uniform(-1,1,(feature_length,num_hidden))
        self.b_hidden = np.random.uniform(-1,1,num_hidden)
        self.b_output = np.random.uniform(-1,1,feature_length)
        return 
    
    
    def FitTheModel(self,X):
        # X is the input values for the variables
        # Rows in x are the samples
        # Cols in x are the features

    