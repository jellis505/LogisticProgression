#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Joe Ellis
# Digital Video & Multimedia Lab
# Logistic Progression

#### Import Libraries #####
import os, sys, getopt, shutil
import subprocess as sub
import shutil
sys.path.append("../utility")
import FileReader as reader
from RunClassification import *
import numpy as np
##########################

#### Global Variables ####
g_audio_dir = "/home/jellis/Project_Data/audio_features/"
g_video_dir = "/home/jellis/Project_Data/core_extraction/"
g_gt_dir = "/home/jellis/Project_Data/ground_truth/"
##########################

def CreateTrainFeatures(features,feat_ids,train_ids):
	# This function returns the features in the returned order of the training ids
	# Do this is the features are stored in a list otherwise we assume they are in a numpy array
	if type(features) == list:
		train_feats = []
		for train_id in train_ids:
			index = feat_ids.index(train_id)
			train_feats.append(features[index])
	# This is for if the values are stored in a numpy array
	else:
		train_feats = np.zeros((len(train_ids),features.shape[1]))
		for i,train_id in enumerate(train_ids):
			index = feat_ids.index(train_id)
			train_feats[i,:] = features[index,:]

	return train_feats

def CreateSVMInput(feats_list,labels):
	# This function creates the feature list for the number of values

def run(argv):
	# This function runs the co-training algorithm for training using unlabeled data

	try:
		opts, args = getopt.getopt(argv,'ht:o:y:')
	except getopt.GetoptError:
		print "You did something wrong"
		sys.exit(0)

	# Parse the arguements in
	train_sample_file = None
	output_newtrain_file = None
	type_of_train = 2
	for opt, arg in opts:
		if opt in ('-h'):
			print "HELP!"
			sys.exit(0)
		elif opt in ('-t'):
			train_sample_file = arg
		elif opt in ('-o'):
			output_newtrain_file = arg
		elif opt in ('-y'):
			type_of_train = int(arg) 

	# Check to make sure that we have the training samples, and the output_file
	if not (train_sample_file and output_newtrain_file):
		print "Didn't input enough stuff"
		sys.exit(0)

	# Read in the samples that we will use for the function	
	with open(train_sample_file,"r") as f:
		raw_lines = f.readlines()
		train_ids = [line.rstrip("\n") for line in raw_lines]

	# Now collect the Audio and Visual Features
	audio_feats,audio_uni_ids = CollectAudioFeats(g_audio_dir)
	video_feats, video_uni_ids = CollectVideoFeats_per_face(g_video_dir,10000)
	gt = GetGroundTruth(g_gt_dir)

	# Now create the training vectors
	train_audio = CreateTrainFeatures(audio_feats,audio_uni_ids,train_ids)
	train_video = CreateTrainFeatures(video_feats,video_uni_ids,train_ids)

	# Now let's get the proper labels for the training
	raw_binary_gt, raw_3way_gt = CreateGTArrays(gt,video_uni_ids)

	# Now choose the labels that we want
	if type_of_train == 2:
		labels = raw_binary_gt
	elif type_of_train == 3:
		labels = raw_3way_gt
	else:
		print "You idiot there is only 2 and three way"
		sys.exit(0)

	#### Train the Audio SVM #####
	train_audio = FeatureNormalization(train_audio)
	audio_svm_clf = trainSVM(audio_train,train_l,8.0,"rbf",.001,True)
	##############################

	#### Train the Video SVM #####
	# Now go through the vector of values and recreate the new one
	norm_video_feats_list = []
	for feat in video_feats:
		norm_feat = np.zeros(feat.shape)
		for z in range(feat.shape[0]):
			norm_feat[z,:] = (feat[z,:] - total_mean) / total_std
		norm_video_feats_list.append(norm_feat)
	train_video_SVM,train_labels = CreateSVMTrainFeats()



	return

if __name__ == "__main__":
	run(sys.argv[1:])