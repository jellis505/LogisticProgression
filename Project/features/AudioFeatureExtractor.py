#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Joe Ellis
# Digital Video & Multimedia Lab
# Logistic Progression

#### Import Libraries ######
import os, sys, getopt
sys.path.append("../utility")
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

	def hamming(self,n):
		#Stolen from the MFCC code
    	return 0.54 - 0.46 * cos(2 * pi / n * (arange(n) + 0.5))

	def ExtractPitchfromFrames(self,frame_secs=0.02,frame_overlap_secs=0.01):
		# This function will extract the fundamental frequency and put it into a numpy array
		# so that we can explore the pitch frequencies present within a signal

		# Values for calculating the samples
		FRAME_LEN = int(frame_secs*self.samp_rate)
		FRAME_OV = int(frame_overlap_secs*self.samp_rate)
		x = self.wav_data
		FFT_SIZE = 2048                         # How many points for FFT
		# This is only used if we want a hamming window on the frame
		#WINDOW = self.hamming(FRAME_LEN)
		
		# We need to make sure that there exists only one channel in the stream, 
		# if there is more then we take the mean of all the channels for our data
		if x.ndim > 1:
			x = np.mean(x,axis=1)

		# Find the number of frames we will have
		f0s = []
		frames = (len(x) - FRAME_LEN) / FRAME_OV + 1
		for i in range(frames):
			
			# This is the window that we will process on
			window = x[i*FRAME_OV : i*FRAME_OV + FRAME_LEN]

			# Now let's find the fft of x
			# The added FFT_SIZE variable zero padds the input so that we get more granularity in the fft
			fftx = np.fft.fft(window, FFT_SIZE)

			# Take the power of each element making the complex go away
			fft_pow = np.abs(fftx ** 2)

			# Find the largest element in the array
			max_freq_index = fft_pow.argmax()

			# Now let's transfrom this back into frequency domain
			fund_freq = (max_freq_index * self.samp_rate) / FFT_SIZE

			# Add our fundamental frequency to the list of frequencies
			f0s.append(fund_freq)

		return np.array(f0s)

	def GetFeaturesfromSeries(self,x):
		# This function takes a series of values and returns the:
		# max, min, mean, and standard deviation of the series
		max_val = np.max(x)
		min_val = np.min(x)
		mean_val = np.mean(x)
		std_val = np.std(x)

		# Return each of these values
		return max_val,min_val,mean_val,std_val




















