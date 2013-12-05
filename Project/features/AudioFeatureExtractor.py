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
import matplotlib.pyplot as plt

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
		val = 0.54 - 0.46 * cos(2 * pi / n * (np.arange(n) + 0.5))
		return val 

	def ExtractPitchfromFrames(self,frame_secs=0.02,frame_overlap_secs=0.01):
		# This function will extract the fundamental frequency and put it into a numpy array
		# so that we can explore the pitch frequencies present within a signal

		# Values for calculating the samples
		FRAME_LEN = int(frame_secs*self.samp_rate)
		FRAME_OV = int(frame_overlap_secs*self.samp_rate)
		x = self.wav_data
		FFT_SIZE = 8192                         # How many points for FFT
		# This is only used if we want a hamming window on the frame
		#WINDOW = self.hamming(FRAME_LEN)
		
		# We need to make sure that there exists only one channel in the stream, 
		# if there is more then we take the mean of all the channels for our data
		if x.ndim > 1:
			x = np.mean(x,axis=1)

		# Find the number of frames we will have
		low_freq = 1500
		total_f0s = []
		low_f0s = []
		upper_f0s = []
		frames = (len(x) - FRAME_LEN) / FRAME_OV + 1
		for i in range(frames):
			
			# This is the window that we will process on
			window = x[i*FRAME_OV : i*FRAME_OV + FRAME_LEN]

			# Now let's find the fft of x
			# The added FFT_SIZE variable zero padds the input so that we get more granularity in the fft
			fftx = np.fft.fft(window, FFT_SIZE)

			# Take the power of each element making the complex go away
			fft_pow = np.abs(fftx ** 2)
			freqs = (np.arange(FFT_SIZE) * self.samp_rate) / FFT_SIZE
			#self.SaveFFTImage(fft_pow,freqs,"/home/jellis/Project_Data/fft.png")

			# Find the largest element in the array
			total_max_freq_index = fft_pow[0:int(FFT_SIZE/2)].argmax()
			under_max_freq_index = fft_pow[0:int(low_freq/(self.samp_rate/FFT_SIZE))].argmax()
			upper_max_freq_index = int(low_freq/(self.samp_rate/FFT_SIZE))+fft_pow[int(low_freq/(self.samp_rate/FFT_SIZE)):int(FFT_SIZE/2)].argmax()

			# Now let's transfrom this back into frequency domain
			fund_freq = (total_max_freq_index * self.samp_rate) / FFT_SIZE
			low_fund_freq = (under_max_freq_index * self.samp_rate) / FFT_SIZE
			upper_fund_freq = (upper_max_freq_index * self.samp_rate) / FFT_SIZE

			# Add our fundamental frequency to the list of frequencies
			low_f0s.append(low_fund_freq)
			upper_f0s.append(upper_fund_freq)
			total_f0s.append(fund_freq)

		return np.array(low_f0s), np.array(total_f0s), np.array(upper_f0s)

	def ExtractEnergyfromFrames(self,frame_secs=0.02,frame_overlap_secs=0.01):
		# This function will extract the fundamental frequency and put it into a numpy array
		# so that we can explore the pitch frequencies present within a signal

		# Values for calculating the samples
		FRAME_LEN = int(frame_secs*self.samp_rate)
		FRAME_OV = int(frame_overlap_secs*self.samp_rate)
		x = self.wav_data
		FFT_SIZE = 8192                         # How many points for FFT
		# This is only used if we want a hamming window on the frame
		#WINDOW = self.hamming(FRAME_LEN)
		
		# We need to make sure that there exists only one channel in the stream, 
		# if there is more then we take the mean of all the channels for our data
		if x.ndim > 1:
			x = np.mean(x,axis=1)

		# Find the number of frames we will have
		low_freq = 1500
		mark = 250 # This is the mark for getting energy below as a feature, this was shown in some 
		# audio emtion detection literature
		bin_width = self.samp_rate / FFT_SIZE
		below_mark_e = []
		total_e = []
		frames = (len(x) - FRAME_LEN) / FRAME_OV + 1
		for i in range(frames):
			# This is the window that we will process on
			window = x[i*FRAME_OV : i*FRAME_OV + FRAME_LEN]

			# Now let's find the fft of x
			# The added FFT_SIZE variable zero padds the input so that we get more granularity in the fft
			fftx = np.fft.fft(window, FFT_SIZE)

			# Take the power of each element making the complex go away
			fft_pow = np.abs(fftx ** 2)
			freqs = (np.arange(FFT_SIZE) * self.samp_rate) / FFT_SIZE

			low_energy = np.sum(fft_pow[0:int(mark/bin_width)])*bin_width
			energy = np.sum(fft_pow[0:int(FFT_SIZE/2)])*bin_width

			below_mark_e.append(low_energy)
			total_e.append(energy)

		return np.array(below_mark_e), np.array(total_e) 


	def GetFeaturesfromSeries(self,x):
		# This function takes a series of values and returns the:
		# max, min, mean, and standard deviation of the series
		max_val = np.max(x)
		min_val = np.min(x)
		mean_val = np.mean(x)
		std_val = np.std(x)

		# Return each of these values
		return [max_val,min_val,mean_val,std_val]

	def SaveFFTImage(self,fft_pow,freqs,filepath):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.plot(freqs,fft_pow)
		ax.ylabel("Power Spectrum")
		ax.xlabel("Frequencies")
		ax.savefig(filepath)
		return

## ENDCLASS

def run(argv):
	# This function runs CoreExtraction for an entire segmented video
	# Now let's parse the arguements
	try:
		opts, args = getopt.getopt(argv,'hi:o:')
	except getopt.GetoptError:
		print "You did something wrong"
		sys.exit(0)

	# Parse the arguements in
	wav_dir = None
	output_dir = None
	for opt, arg in opts:
		if opt in ('-h'):
			print "HELP!"
			sys.exit(0)
		elif opt in ('-i'):
			wav_dir = arg
		elif opt in ('-o'):
			output_dir = arg

	# Check to make sure that the output are sufficient
	if not (wav_dir and output_dir):
		print "You did not include either the video_dir or the output_dir"
		sys.exit(0)

	# Let's get all of the videos here that are in the directory
	files = os.listdir(wav_dir)
	wavs = [file_ for file_ in files if ".wav" in file_]
	wav_paths = [os.path.join(wav_dir,wav) for wav in wavs]

	# Now let's loop through the videos and process them
	
	# DEBUG 
	print wav_paths

	for wav_path in wav_paths:
		
		# Extract the features
		ae = AudioExtractor(wav_path)
		mfccs = ae.CalculateMFCCs()
		low_fund_freqs,fund_freqs,upper_fund_freqs = ae.ExtractPitchfromFrames()
		low_E, total_E = ae.ExtractEnergyfromFrames()
		
		# Now that we have the total frames for this wavfile let's create the audio feature
		audio_feat = []
		audio_feat.extend(ae.GetFeaturesfromSeries(low_fund_freqs))
		audio_feat.extend(ae.GetFeaturesfromSeries(fund_freqs))
		audio_feat.extend(ae.GetFeaturesfromSeries(upper_fund_freqs))
		audio_feat.extend(ae.GetFeaturesfromSeries(low_E))
		audio_feat.extend(ae.GetFeaturesfromSeries(total_E))
		for i in range(mfccs.shape[1]):
			audio_feat.extend(ae.GetFeaturesfromSeries(mfccs[i,:]))
		a_feat = np.array(audio_feat)

		# Create the output files
		file_only = reader.GetFileOnly(wav_path)
		file_aud_ext = reader.ReplaceExt(file_only,".audio_feat")
		output_path = os.path.join(output_dir,file_aud_ext)

		# Here is where we extract the features
		# Now let's save the feature that we have just extracted from this audio segment using 
		np.savetxt(output_path,a_feat,delimiter=",")

	return

if __name__ == "__main__":
	run(sys.argv[1:])
