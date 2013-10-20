#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# News Rover System
# Digital Video & Multimedia Lab
# Columbia University

import pylab
import matplotlib.pyplot as plt
import math

def PlotNGraph(x_vec,y_vec):
    plt.plot(x_vec,y_vec)
    plt.ylabel("Perplexity per gram")
    plt.title("Average Perplexity of Seen Grams in our Dev Set")
    plt.xlabel("N-Gram Parameter (N)")
    plt.show()
    plt.savefig("Perp.png")
    
if __name__ == "__main__":
    # This plots the graph of the average perplexity of each seen value
    x_vec = range(1,7)
    
    ### A Tale of Two Cities ###
    ### This section holds the possible y_vectors we have for our graphs
    # This is the seen entropy vectors w/no smoothing
    y_vec_entropy = [-0.04,-0.0056,-0.0049,-0.025,-0.146,-0.796229]
    
    # This is with Laplace smoothing of our values
    #OVer seen variables
    y_vec_entropy = [-0.049069,-0.005610,-0.004953,-0.025082,-0.146381,-0.796229]
    #Over all n-grams in dev
    y_vec_entropy = [-0.046434,-0.003358,-0.001034,-0.001092,-0.001119,-0.001124]
    
    #
    
    
    ### The Scarlet Letter ###
    
    
    y_vec_perp = []
    for val in y_vec_entropy:
        y_vec_perp.append(math.pow(2,-val))
    
    # Now plot the graph
    PlotNGraph(x_vec[0:5],y_vec_perp[0:5])
    
    
