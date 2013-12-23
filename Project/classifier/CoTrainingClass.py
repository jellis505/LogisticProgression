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
from scipy.spatial.distance import pdist
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

def GetUnlabeledFeatures(audio_feats,video_list,train_ids,audio_ids,video_ids,test_ids):
	# This creates labels of the unlabeled features
	u_video_feat_list = []
	r = train_ids + test_ids
	unlabeled_ids = [audio_id for audio_id in audio_ids if audio_id not in r]
	u_audio_feats = np.zeros((len(unlabeled_ids),audio_feats.shape[1])) 
	for i,audio_id in enumerate(unlabeled_ids):
		ai = audio_ids.index(audio_id)
		u_audio_feats[i,:] = audio_feats[ai,:]
		vi = video_ids.index(audio_id)
		u_video_feat_list.append(video_list[vi])

	return u_audio_feats, u_video_feat_list, unlabeled_ids

def OutputUnlabeledFile(file_id,bin_,labels,top_vals,output_file):
	# This function outputs to the new file the proper values
	# This function rocks!
	if bin_ == True:
		with open(output_file,"w") as f:
			for id_,label,top_val in zip(file_id,labels,top_vals):
				output_string = "%s,0,%d,%d\n" % (id_,label,top_val)
				f.write(output_string)
	else:
		with open(output_file,"r") as f:
			for id_,label,top_val in zip(file_id,labels,top_vals):
				output_string = "%s,0,%d,%d\n" % (id_,label,top_val)
				f.write(output_string)

	return

def testSVM_max_vote2(svm_clf,test,test_labels,get_probs=False):
	# This tests the accuracy of the built classifier
	#prob_vals = np.zeros((len(test),2))
	#perc_pred_labels = []
	desc_funcs = []
	for i,test1 in enumerate(test):
		#pred_labels = svm_clf.predict(test1)
		desc_func = svm_clf.decision_function(test1)
		if len(desc_func) == 0:
			desc_funcs.append[0]
		else:
			desc_funcs.append(np.sum(desc_func))
	return desc_funcs

def GetDistancetoDecisionFunction(svm_clf,feats):
	# Gets the distance to the decision function
	return svm_clf.decision_function(feats)

def ReturnSamples(a_list,v_list,unlabeled_ids,percent):
	# Find the samples that are most represenative of each section
	percent = percent/2.;
	num_samples = int(np.floor(len(a_list)*percent))
	print num_samples
	new_neg_train_labels = []
	for a in a_list[:num_samples]:
		if float(a[1]) < 0:
			new_neg_train_labels.append(unlabeled_ids[a[0]])
		else:
			break
	for v in v_list[:num_samples]:
		if v[1] < 0:
			new_neg_train_labels.append(unlabeled_ids[v[0]])
		else:
			break

	new_pos_train_labels = []
	for a in a_list[len(a_list)-num_samples:]:
		if float(a[1]) > 0:
			new_pos_train_labels.append(unlabeled_ids[a[0]])
		else:
			break

	for v in v_list[len(v_list)-num_samples:]:
		if v[1] > 0:
			new_pos_train_labels.append(unlabeled_ids[v[0]])
		else:
			break

	return new_pos_train_labels,new_neg_train_labels

def GetGroundTruthFile(file_):
	gt = {}
	with open(file_,"r") as f:
		raw_lines = f.readlines()
		lines_ = [line.rstrip("\r\n") for line in raw_lines]
		lines = [line.rstrip("\n") for line in lines_]
		train_ids = []
		for line in lines:
			parts = line.split(',')
			# Add this section to the dictionary we are creating
			gt[parts[0]] = {"3-way" : int(parts[1]), "binary" : int(parts[2]), "Good?" : int(parts[3])}
			if int(parts[3]) == 1:
				train_ids.append(parts[0])
	return gt, train_ids

def run(argv):
	# This function runs the co-training algorithm for training using unlabeled data

	try:
		opts, args = getopt.getopt(argv,'ht:o:y:r:')
	except getopt.GetoptError:
		print "You did something wrong"
		sys.exit(0)

	# Parse the arguements in
	train_sample_file = None
	output_newtrain_file = None
	type_of_train = 2
	unlabeled_file = None
	test_gt_file = None
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
		elif opt in ('-u'):
			unlabeled_file = arg
		elif opt in ('-r'):
			test_gt_file = arg

	# Check to make sure that we have the training samples, and the output_file
	if not (train_sample_file and output_newtrain_file):
		print "Didn't input enough stuff"
		sys.exit(0)

	# Now collect the Audio and Visual Features
	audio_feats,audio_uni_ids = CollectAudioFeats(g_audio_dir)
	video_feats, video_uni_ids = CollectVideoFeats_per_face(g_video_dir,10000)
	#gt = GetGroundTruth(g_gt_dir)

	gt, train_ids = GetGroundTruthFile(train_sample_file)
	print len(train_ids)
	gt_test, test_ids = GetGroundTruthFile(test_gt_file)

	# Now create the training vectors
	train_audio = CreateTrainFeatures(audio_feats,audio_uni_ids,train_ids)
	train_video = CreateTrainFeatures(video_feats,video_uni_ids,train_ids)


	# Now get the untrained labels
	if not unlabeled_file:
		u_audio_feat, u_video_feat_list, unlabeled_ids = GetUnlabeledFeatures(audio_feats,video_feats,train_ids,audio_uni_ids,video_uni_ids,test_ids)
	print "The number of unlabeled videos is: ", len(unlabeled_ids)

	# Now let's get the proper labels for the training
	raw_binary_gt, raw_3way_gt = CreateGTArrays(gt,train_ids)

	# Now choose the labels that we want
	if type_of_train == 2:
		labels = raw_binary_gt
	elif type_of_train == 3:
		labels = raw_3way_gt
	else:
		print "You idiot there is only 2 and three way"
		sys.exit(0)

	#### Train the Audio SVM #####
	train_audio,mean_audio,std_audio = FeatureNormalization(train_audio)
	
	# Calculate the Standard deviation of the points
	Y = pdist(train_audio,'euclidean')
	print Y
	print np.mean(Y)
	gamma = np.mean(Y)
	audio_svm_clf = trainSVM(train_audio,labels,8,"rbf",.007)
	##############################

	#### Train the Video SVM #####
	# Now go through the vector of values and recreate the new one
	# Normalize across all total values of vidual features
	big_ass_feat_vec = train_video[0]
	for feat in train_video[1:]:
		# Now let's create one big ass vector of features
		big_ass_feat_vec = np.vstack((big_ass_feat_vec,feat))

	# Now let's find the total feature vector standard deviation and mean of the material
	total_std = np.std(big_ass_feat_vec,axis=0)
	total_mean = np.mean(big_ass_feat_vec,axis=0)

	# make sure all of our features have some element of standard deviation
	zeros = total_std < np.finfo(float).eps
	for j,zero in enumerate(zeros):
		if zero:
			total_std[j] = 1.00

	norm_video_feats_list = []
	for feat in train_video:
		norm_feat = np.zeros(feat.shape)
		for z in range(feat.shape[0]):
			norm_feat[z,:] = (feat[z,:] - total_mean) / total_std
		norm_video_feats_list.append(norm_feat)
	train_video_SVM,train_labels = CreateSVMTrainFeats(norm_video_feats_list,labels)

	# Calculate the Standard Deviation of the Points
	Y = pdist(train_video_SVM,'euclidean')
	print Y
	print np.mean(Y)
	gamma = np.mean(Y)
	vid_svm_clf = trainSVM(train_video_SVM,train_labels,8,"linear",.0007)
	################################

	###### Get UnLabeled Audio Probability ####
	# Feature Normalization
	u_audio_norm_feats = np.zeros(u_audio_feat.shape)
	for i in range(u_audio_norm_feats.shape[0]):
		u_audio_norm_feats[i,:] = (u_audio_feat[i,:] - mean_audio) / std_audio

	dummy_list = [1 for i in range(u_audio_norm_feats.shape[0])]
	a_pred_labels,acc = testSVM(audio_svm_clf,u_audio_norm_feats,dummy_list,False)
	a_dist_to_desc = GetDistancetoDecisionFunction(audio_svm_clf,u_audio_norm_feats)
	#for pred_label,dist in zip(pred_labels,a_dist_to_desc):
	#	print pred_label,dist
	###########################################

	###### Get Unlabeled Video Probability ####
	u_norm_video_feats_list = []
	for feat in u_norm_video_feats_list:
		norm_feat = np.zeros(feat.shape)
		for z in range(feat.shape[0]):
			norm_feat[z,:] = (feat[z,:] - total_mean) / total_std
		u_norm_video_feats_list.append(norm_feat)
	
	# Now get the probabilities
	if type_of_train == 2:
		v_dist_to_desc = testSVM_max_vote2(vid_svm_clf,u_norm_video_feats_list,[-1,1],True)
		u_video_labels, acc = testSVM_max_vote(vid_svm_clf,u_norm_video_feats_list,dummy_list,False)
	else:
		video_probs = testSVM_max_vote(vid_svm_clf,u_norm_video_feats_list,[-1,0,1],True)
		#video_probs = testSVM_max_vote2(vid_svm_clf,u_norm_video_feats_list,[-1,1],True)
	#for i in range(len(v_dist_to_desc)):
	#	print v_dist_to_desc[i]
	###########################################

	#### Video Selection (Audio) #####
	a_tuple_desc_funcs = enumerate(a_dist_to_desc)
	a_rising = sorted(a_tuple_desc_funcs, key=lambda tup: tup[1])
	#a_decsending = sorted(a_tuple_desc_funcs, key=lambda tup: tup[1],reverse=True)
	#print a_rising
	###################################

	#### Video Selection (Video) #####
	v_tuple_desc_funcs = enumerate(v_dist_to_desc)
	v_rising = sorted(v_tuple_desc_funcs, key=lambda tup: tup[1])
	#v_descending = sorted(v_tuple_desc_funcs, key=lambda tup: tup[1],reverse=True)
	#print v_rising
	###################################

	#### Get the positive samples to add #####
	pos,neg = ReturnSamples(a_rising,v_rising,unlabeled_ids,0.2)
	pos = set(pos)
	neg = set(neg)

	print len(pos)
	print len(neg)

	##### Now Create the new output files ####
	output_ids = train_ids + list(pos) + list(neg)
	output_labels = list(labels) + [1 for i in range(len(pos))] + [-1 for i in range(len(neg))]
	use = [1 for i in output_labels]
	non_used_ids = [u_id for u_id in unlabeled_ids if u_id not in output_ids]
	output_ids = output_ids + non_used_ids
	output_labels = output_labels + [0 for i in non_used_ids]
	use = use + [-1 for i in non_used_ids]

	print len(output_labels)
	print len(output_ids)
	print len(use)

	# Output to a file to use for co-training
	OutputUnlabeledFile(output_ids,True,output_labels,use,output_newtrain_file)

	#### This section runs the training
	test_audio = CreateTrainFeatures(audio_feats,audio_uni_ids,test_ids)
	test_video = CreateTrainFeatures(video_feats,video_uni_ids,test_ids)
	# Now let's get the proper labels for the testing
	raw_binary_gt_test, raw_3way_gt_test = CreateGTArrays(gt_test,test_ids)

	##### Get Accuracy over Audio Files #########
	norm_test_audio = np.zeros(test_audio.shape)
	for i in range(norm_test_audio.shape[0]):
		norm_test_audio[i,:] = (test_audio[i,:] - mean_audio) / std_audio
	a_pred_labels,acc = testSVM(audio_svm_clf,norm_test_audio,raw_binary_gt_test,False)
	print a_pred_labels
	print "The Audio Classification Accuracy is: ", acc
	##############################################

	##### Get the Accuracy over Visual Features###
	norm_test_video_list = []
	for feat in test_video:
		norm_feat = np.zeros(feat.shape)
		for z in range(feat.shape[0]):
			norm_feat[z,:] = (feat[z,:] - total_mean) / total_std
		norm_test_video_list.append(norm_feat)
	video_pred_labels, acc = testSVM_max_vote(vid_svm_clf,norm_test_video_list,raw_binary_gt_test,False)
	print video_pred_labels
	print "The Video Classification Accuracy is: ", acc

	return

if __name__ == "__main__":
	run(sys.argv[1:])