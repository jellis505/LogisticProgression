#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Joe Ellis
# Digital Video & Multimedia Lab
# Logistic Progression

#### Import Libraries ######
import os, sys, getopt
import subprocess as sub
import shutil
sys.path.append("utility")
import FileReader as reader
from scipy.io import wavfile
import numpy as np
import MFCC


##### Global Variables #######

class AudioExtractor():
	def __init__(self, wav_path):
		self.wav_path = wav_path
		self.samp_rate, self.wav_data = wavfile.read(wav_path)
		return 

	def CalculateMFCCs(self):
		# This function calculates and returns the MFCC from the given wavfile
		mfccs = MFCC.extract(self.wav_data)
		return mfccs

	def GetWavStatistics(self):
		# This will calculate some statistics about the 
		
		# Calculate the Mean
		mean_data = np.mean(self.wav_data, axis=1)
		mean_volume = np.mean(mean_data)

		# Now calculate the standard deviation of the volume
		std_data = np.std(mean_data)

		return mean_volume, std_data










