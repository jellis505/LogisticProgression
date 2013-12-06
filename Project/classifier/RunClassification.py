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
import math



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

def CreateGTArrays(gt,uni_ids):
	#This will create the ground truth arrays that we want for testing the data
	raw_binary_gt = np.zeros(len(uni_ids))
	raw_3way_gt = np.zeros(len(uni_ids))
	for i,uni_id in enumerate(uni_ids):
		raw_binary_gt[i] = gt[uni_id]["binary"]
		raw_3way_gt[i] = gt[uni_id]["3-way"]

	return raw_binary_gt, raw_3way_gt

def trainSVM(train,train_labels,C=1,kernel="rbf",gamma=1):
	# This trains the parameters, see the scikit-learn documentation for usage
	svm_clf = svm.SVC(C,kernel,0,gamma)
	#print svm_clf
	svm_clf.fit(train,train_labels)
	return svm_clf

def testSVM(svm_clf,test,test_labels):
	# This tests the accuracy of the built classifier
	pred_labels = svm_clf.predict(test)
	correct = np.sum(pred_labels == test_labels)
	acc = correct / float(len(test_labels))
	return pred_labels, acc

def SepTrainandTest(feats,labels,split):
	# Check to make sure that the split is less than 1
	if split > 1 or split < 0:
		print "You moron you can't split data you don't have!"

	# now let's create a permutation of the data
	num_points = len(labels)
	perm = np.random.permutation(num_points)
	train_index = perm[0:int(split*num_points)]
	test_index = perm[int(split*num_points):]
	train = feats[train_index,:]
	train_labels = labels[train_index]
	test = feats[test_index,:]
	test_labels = labels[test_index,:]
	
	return train,train_labels,test,test_labels

def FeatureNormalization(feats):
	# This will do a standard feature normalization, by subtracting the mean from each dim
	# and then normalizing by the standard deviation
	std_feats = np.std(feats,axis=0)
	mean_feats = np.mean(feats,axis=0)

	# We have one of the features with no variance... Feature sucks.
	std_feats[9] = 1.000

	# Normalized Features
	norm_feats = np.zeros(feats.shape)

	for i in range(norm_feats.shape[0]):
		norm_feats[i,:] = (feats[i,:] - mean_feats) / std_feats
	return norm_feats

def GetGoodVideos(gt,uni_ids):
	# This returns the videos that we have marked as very good
	# 


if __name__ == "__main__":
	# Main function runs classification
	audio_dir = "/home/jellis/Project_Data/audio_features"
	gt_dir = "/home/jellis/Project_Data/ground_truth"
	audio_feats,uni_ids = CollectAudioFeats(audio_dir)
	gt = GetGroundTruth(gt_dir)
	
	# Test uni_ids
	uni_tests = [uni_id for uni_id in uni_ids if uni_id[0:uni_id.rfind("_")] in ["fcSJd9BfqSk","Oo0GGfpPzOA","z5vLvo9yXpA"]]
	# Find the good indices for the np array
	good_indices = [i for i,id_ in enumerate(uni_ids) if id_[0:id_.rfind("_")] in ["fcSJd9BfqSk","Oo0GGfpPzOA","z5vLvo9yXpA"]]
	
	great_videos = 

	# Now check the audio feats from the ones that we actually have
	curr_audio_feats = audio_feats[good_indices,:]
	norm_audio_feats = FeatureNormalization(curr_audio_feats)

	# Return the labels
	raw_binary_gt, raw_3way_gt = CreateGTArrays(gt,uni_tests)

	####### This section of the code is for multiple tests ###########
	# Let's create the C and rbf values to figure out what is the best
	C_arr = 10 ** np.arange(-5,5,dtype=float)
	gamma_arr = 10 ** np.arange(-5,5,dtype=float)
	print gamma_arr
	test_nums = 30

	for i in range(len(C_arr)):
		for j in range(len(gamma_arr)):
			acc_vec = np.zeros(test_nums)
			for k in range(test_nums):
				# Seperate the Training and Testing
				train,train_l,test,test_l = SepTrainandTest(norm_audio_feats,raw_3way_gt,0.7)

				# Now train the SVM
				svm_clf = trainSVM(train,train_l,C_arr[i],"rbf",gamma_arr[j])

				# Now test the values
				pred_labels,acc = testSVM(svm_clf,test,test_l)
				acc_vec[k] = acc

			print "The Mean Acc for C=%f and gamma=%f is %f" % (C_arr[i],gamma_arr[j],np.mean(acc_vec))



