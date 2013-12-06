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
	# Let's collect the video features
	dirs = [os.path.join(video_dir, o) for o in os.listdir(video_dir)]
	ids = [reader.GetFileOnly(o) for o in dirs]

	# Now let's get the features for each video
	feature_dirs = [os.path.join(o,"features") for o in dirs]
	face_files = [os.path.join(a,b + ".face") for a,b in zip(dirs,ids)]

	for feat_dir,face_file in zip(feature_dirs,face_files):
		# Let's Read in the face file
		faces = reader.ReadFaceFile(face_file)

		# This portion of code will analyze the face files, and decide which are good faces
		# that contain the features that we want to use, we need to do this because we want faces to be 
		# consistent and only use the main face for feature extraction
		detected_face_frames = [face[0] for face in faces]
		detected_face_frames = list(set(detected_face_frames))
		faces_by_frame = [[] for f in detected_face_frames]
		for face in faces:
			faces_by_frame[detected_face_frames.index(face[0])].append(face)
		faces_by_frame.sort()
		
		# Now let's track the motion of the faces, and we will only use the images from the good faces
		


	return None,None

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
	# This returns the videos that we have marked as very good,
	good_indexs = []
	for i,id_ in enumerate(uni_ids):
		if gt[id_]["Good?"] == 1:
			good_indexs.append(i)
	return good_indexs


if __name__ == "__main__":
	# Main function runs classification
	audio_dir = "/home/jellis/Project_Data/audio_features"
	gt_dir = "/home/jellis/Project_Data/ground_truth"
	video_dir = "/home/jellis/Project_Data/core_extraction"
	video_feats, ids = CollectVideoFeats(video_dir) 
	quit()


	audio_feats,uni_ids = CollectAudioFeats(audio_dir)
	gt = GetGroundTruth(gt_dir)
	
	# Test uni_ids
	uni_tests = [uni_id for uni_id in uni_ids if uni_id[0:uni_id.rfind("_")] in ["fcSJd9BfqSk","Oo0GGfpPzOA","z5vLvo9yXpA"]]
	# Find the good indices for the np array
	good_indices = [i for i,id_ in enumerate(uni_ids) if id_[0:id_.rfind("_")] in ["fcSJd9BfqSk","Oo0GGfpPzOA","z5vLvo9yXpA"]]
	
	# Now check the audio feats from the ones that we actually have
	curr_audio_feats = audio_feats[good_indices,:]
	norm_audio_feats = FeatureNormalization(curr_audio_feats)

	# Return the labels
	raw_binary_gt, raw_3way_gt = CreateGTArrays(gt,uni_tests)


	# This portion is for only if we want to use the videos marked good
	# These are the videos that we marked as good videos
	#great_videos = GetGoodVideos(gt,uni_tests)
	#print len(great_videos)
	#norm_audio_feats = norm_audio_feats[great_videos,:]
	#raw_binary_gt = raw_binary_gt[great_videos]
	#raw_3way_gt = raw_3way_gt[great_videos]


	####### This section of the code is for multiple tests ###########
	# Let's create the C and rbf values to figure out what is the best
	C_arr = 2 ** np.arange(0,10,dtype=float)
	gamma_arr = 2 ** np.arange(-10,0,dtype=float)
	test_nums = 100

	max_acc = 0
	max_C = 0
	max_gamma = 0

	for i in range(len(C_arr)):
		for j in range(len(gamma_arr)):
			acc_vec = np.zeros(test_nums)
			for k in range(test_nums):
				# Seperate the Training and Testing
				train,train_l,test,test_l = SepTrainandTest(norm_audio_feats,raw_3way_gt,0.9)

				# Now train the SVM
				svm_clf = trainSVM(train,train_l,C_arr[i],"rbf",gamma_arr[j])

				# Now test the values
				pred_labels,acc = testSVM(svm_clf,test,test_l)
				acc_vec[k] = acc

			# Check to see if this is the best configuration
			if np.mean(acc_vec) > max_acc:
				max_acc = np.mean(acc_vec)
				max_C = C_arr[i]
				max_gamma = gamma_arr[j]

			print "The Mean Acc for C=%f and gamma=%f is %f" % (C_arr[i],gamma_arr[j],np.mean(acc_vec))

	print "The max accuracy is: ", max_acc
	print "The best C is: ", max_C
	print "The best gamma is: ", max_gamma



