#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Joe Ellis
# Digital Video & Multimedia Lab
# Logistic Progression

#### Import Libraries
import os, sys, getopt
from sklearn import svm
import numpy as np
sys.path.append('../utility')
import FileReader as reader

def CollectAudioFeats(audio_dir):
	# This function collects all of the audio features, and puts them into a numpy array
	# This all returns the video that each feature is extracted from
	files = [os.path.join(audio_dir,o) for o in os.listdir(audio_dir)]
	files_only = [reader.GetFileOnly(o) for o in files]
	uni_ids = [reader.ReplaceExt(o,"") for o in files_only]

	# Now that we have the list of unique identifiers for each value let's read in the files
	# Load the first value so we can vstack the rest of them
	data_array = np.loadtxt(files[0])
	for file_ in files[1:]:
		# Now let's create the np array here
		a = np.loadtxt(file_)
		data_array = np.vstack((data_array,a))

	# Now we have the data array form the audio features
	return data_array,uni_ids

def CollectVideoFeats(video_dir):
	pass

def GetGroundTruth(gt_dir):
	files = [os.path.join(gt_dir,o) for o in os.listdir(gt_dir)]

	# Now let's read the files
	gt = {}
	for file_ in files:
		with open(file_,"r") as f:
			raw_lines = f.readlines()
			lines_ = [line.rstrip("\r\n") for line in raw_lines]
			lines = [line.rstrip("\n") for line in lines_]
			for line in lines:
				parts = line.split(',')
				# Add this section to the dictionary we are creating
				gt[parts[0]] = {"3-way" : int(parts[1]), "binary" : int(parts[2]), "Good?" : int(parts[3])}

	return gt

def 

def CreateGTArrays(gt,uni_ids):
	#This will create the ground truth arrays that we want for testing the data
	raw_binary_gt = np.array
	raw_3way_gt = np.array
	for i,uni_id in enumerate(uni_ids):
		raw_binary_gt[i] = gt[uni_id]["binary"]
		raw_3way_gt[i] = gt[uni_id]["3-way"]

	return raw_binary_gt, raw_3way_gt 

if __name__ == "__main__":
	# Main function runs classification
	audio_dir = "/home/jellis/Project_Data/audio_features"
	gt_dir = "/home/jellis/Project_Data/ground_truth"
	audio_feats,uni_ids = CollectAudioFeats(audio_dir)
	gt = GetGroundTruth(gt_dir)
	
	# Test uni_ids
	uni_tests = [uni_id for uni_id in uni_ids if uni_id[0:uni_id.rfind("_")] in ["fcSJd9Bfqsk","Oo0GGfpPzOA","z5vLv09yXpA"]]
	
	# Return the labels
	raw_binary_gt, raw_3way_gt = CreateGTArrays(gt,uni_tests)
