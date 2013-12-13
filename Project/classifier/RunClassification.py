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
import copy

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

def CollectVideoFeats_mean_std(video_dir,size_thresh):
	# Let's collect the video features
	dirs = [os.path.join(video_dir, o) for o in os.listdir(video_dir)]
	ids = [reader.GetFileOnly(o) for o in dirs]

	# Now let's get the features for each video
	feature_dirs = [os.path.join(o,"features") for o in dirs]
	face_files = [os.path.join(a,b + ".face") for a,b in zip(dirs,ids)]

	# This is the value tha twe will return
	overall_face_feats = np.zeros((len(ids),1664*2+1))
	
	for z,(feat_dir,face_file) in enumerate(zip(feature_dirs,face_files)):
		# Let's Read in the face file
		faces = reader.ReadFaceFile(face_file)

		# This portion of code will analyze the face files, and decide which are good faces
		# that contain the features that we want to use, we need to do this because we want faces to be 
		# consistent and only use the main face for feature extraction
		detected_face_frames = [face[0] for face in faces]
		detected_face_frames = list(set(detected_face_frames))
		faces_by_frame = [[] for f in detected_face_frames]
		for k,face in enumerate(faces):
			faces_by_frame[detected_face_frames.index(face[0])].append(face)
		faces_by_frame.sort()
		
		# Now let's track the motion of the faces, and we will only use the images from the good faces
		# aka we use the largest detected face on the screen each time
		good_faces = []
		for faces in faces_by_frame:
			orig_order = copy.copy(faces)
			faces.sort(key=lambda tup : -(tup[3]*tup[4]))
			if faces[0][3]*faces[0][4] > size_thresh:
				faces[0][0] = (orig_order.index(faces[0]),faces[0][0])
				good_faces.append(faces[0])

		# Now let's get the head motion per frame
		# Let's loop through each little thing to get the head motion
		if len(good_faces) > 1:
			motion_per_frame = []
			for i in range(1,len(good_faces)):
				curr_pos = (good_faces[i][1]+int(good_faces[i][3]/2),good_faces[i][2]+int(good_faces[i][4]/2))
				last_pos = (good_faces[i-1][1]+int(good_faces[i-1][3]/2),good_faces[i-1][2]+int(good_faces[i-1][4]/2))
				motion = np.sqrt((curr_pos[0]-last_pos[0]) ** 2 + (curr_pos[1]-last_pos[1]) ** 2)
				elapsed_frames = good_faces[i][0][1]-good_faces[i-1][0][1]
				motion_per_frame.append(motion/float(elapsed_frames))

			# This should be the average fame motion throughout the frame
			avg_motion = np.mean(np.array(motion_per_frame))

			# Now let's read in all of the sections of the frames
			raw_faces = np.zeros((len(good_faces),1664))
			for j,good_face in enumerate(good_faces):
				face_file = os.path.join(feat_dir,str(good_face[0][1]) + "_" + str(good_face[0][0]) + ".feat")
				array = reader.ReadFaceFeatures(face_file)
				raw_faces[j,:] = np.array(array)

			face_means = np.mean(raw_faces, axis=0)
			face_stds = np.mean(raw_faces,axis=0)

			# This creates the area where we add the values to the final data array
			overall_face_feats[z,:] = np.hstack((face_means,face_stds,avg_motion))

	return overall_face_feats,ids

def CollectVideoFeats_per_face(video_dir,size_thresh):
	# Let's collect the video features
	dirs = [os.path.join(video_dir, o) for o in os.listdir(video_dir)]
	ids = [reader.GetFileOnly(o) for o in dirs]

	# Now let's get the features for each video
	feature_dirs = [os.path.join(o,"features") for o in dirs]
	face_files = [os.path.join(a,b + ".face") for a,b in zip(dirs,ids)]
	
	face_arrays = []
	for z,(feat_dir,face_file) in enumerate(zip(feature_dirs,face_files)):
		# Let's Read in the face file
		faces = reader.ReadFaceFile(face_file)

		# This portion of code will analyze the face files, and decide which are good faces
		# that contain the features that we want to use, we need to do this because we want faces to be 
		# consistent and only use the main face for feature extraction
		detected_face_frames = [face[0] for face in faces]
		detected_face_frames = list(set(detected_face_frames))
		faces_by_frame = [[] for f in detected_face_frames]
		for k,face in enumerate(faces):
			faces_by_frame[detected_face_frames.index(face[0])].append(face)
		faces_by_frame.sort()
		
		# Now let's track the motion of the faces, and we will only use the images from the good faces
		# aka we use the largest detected face on the screen each time
		good_faces = []
		for faces in faces_by_frame:
			orig_order = copy.copy(faces)
			faces.sort(key=lambda tup : -(tup[3]*tup[4]))
			if faces[0][3]*faces[0][4] > size_thresh:
				faces[0][0] = (orig_order.index(faces[0]),faces[0][0])
				good_faces.append(faces[0])

		# Now let's get the head motion per frame
		# Let's loop through each little thing to get the head motion
		if len(good_faces) > 1:
			motion_per_frame = []
			for i in range(1,len(good_faces)):
				curr_pos = (good_faces[i][1]+int(good_faces[i][3]/2),good_faces[i][2]+int(good_faces[i][4]/2))
				last_pos = (good_faces[i-1][1]+int(good_faces[i-1][3]/2),good_faces[i-1][2]+int(good_faces[i-1][4]/2))
				motion = np.sqrt((curr_pos[0]-last_pos[0]) ** 2 + (curr_pos[1]-last_pos[1]) ** 2)
				elapsed_frames = good_faces[i][0][1]-good_faces[i-1][0][1]
				motion_per_frame.append(motion/float(elapsed_frames))

			# This should be the average fame motion throughout the frame
			avg_motion = np.mean(np.array(motion_per_frame))

			raw_faces = np.zeros((len(good_faces),896))
			for j,good_face in enumerate(good_faces):
				face_file = os.path.join(feat_dir,str(good_face[0][1]) + "_" + str(good_face[0][0]) + ".feat")
				array = reader.ReadFaceFeatures(face_file)
				raw_faces[j,:] = np.array(array)

			# Now let's create a list of numpy arrays that hold the faces
			face_arrays.append(raw_faces)
		else:
			face_arrays.append(np.zeros((1,896)))

	return face_arrays, ids 

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

def trainSVM(train,train_labels,C=1,kernel="rbf",gamma=1,probability_val=False):
	# This trains the parameters, see the scikit-learn documentation for usage
	svm_clf = svm.SVC(C,kernel,0,gamma,probability=probability_val)
	#print svm_clf
	svm_clf.fit(train,train_labels)
	return svm_clf

def testSVM_max_vote(svm_clf,test,test_labels,get_probs=False):
	# This tests the accuracy of the built classifier
	maj_pred_labels = []
	for test1 in test:
		
		# Get the predicted labels
		pred_labels = svm_clf.predict(test1)
		
		# Find the majority class
		zero_class_sum = np.sum(pred_labels == 0)
		neg_class_sum = np.sum(pred_labels == -1)
		pos_class_sum = np.sum(pred_labels == 1)

		if (pos_class_sum >= zero_class_sum) and (pos_class_sum >= neg_class_sum):
			maj_pred_labels.append(1.0)
		elif (neg_class_sum >= zero_class_sum) and (neg_class_sum >= pos_class_sum):
			maj_pred_labels.append(-1.0)
		else:
			maj_pred_labels.append(0.0)

	# Now find out how many of our majority voted labels work
	correct = np.sum(np.array(maj_pred_labels) == np.array(test_labels))

	acc = correct / float(len(test_labels))
	return maj_pred_labels, acc



def testSVM(svm_clf,test,test_labels,get_probs=False):
	# This tests the accuracy of the built classifier
	
	if get_probs == False:
		pred_labels = svm_clf.predict(test)
		correct = np.sum(pred_labels == test_labels)

		acc = correct / float(len(test_labels))
		return pred_labels, acc
	else:
		probs = svm_clf.predict_proba(test)
		return probs

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

def SepTrainandTest2(feats_list,labels,split):
	# This is the second version of train and test split that actually uses the 
	if split > 1 or split < 0:
		print "You moron you can't split data you don't have"
		sys.exit(0)

	# Now let's create a permutation of the feature_list data
	num_points = len(labels)
	perm = np.random.permutation(num_points)
	train_index = perm[0:int(split*num_points)]
	test_index = perm[int(split*num_points):]
	
	train = []
	train_labels = []
	for item in train_index:
		train.append(feats_list[item])
		train_labels.append(labels[item])

	test = []
	test_labels = [] 
	for item in test_index:
		test.append(feats_list[item])
		test_labels.append(labels[item])
	
	# Create the face features used for training values for this given work
	train_SVM,train_l = CreateSVMTrainFeats(train,train_labels)

	return train_SVM,train_l,test,test_labels

def CreateSVMTrainFeats(train_list,labels):
	train = train_list[0]
	train_l = np.empty(train.shape[0])
	train_l.fill(labels[0])

	for (train_feat,label) in zip(train_list[1:],labels[1:]):
		train = np.vstack((train,train_feat))
		train_l1 = np.empty(train_feat.shape[0])
		train_l1.fill(label)
		train_l = np.append(train_l,train_l1)

	return train,train_l


def FeatureNormalization(feats):
	# This will do a standard feature normalization, by subtracting the mean from each dim
	# and then normalizing by the standard deviation
	std_feats = np.std(feats,axis=0)
	mean_feats = np.mean(feats,axis=0)

	# We have one of the features with no variance... Feature sucks.
	# we need to make sure we don't have any zero valued features
	zeros = std_feats < np.finfo(float).eps
	for j,zero in enumerate(zeros):
		if zero:
			std_feats[j] = 1.00

	# Normalized Features
	norm_feats = np.zeros(feats.shape)

	for i in range(norm_feats.shape[0]):
		norm_feats[i,:] = (feats[i,:] - mean_feats) / std_feats
	return norm_feats

def GetGoodVideos(gt,uni_ids):
	# This returns the videos that we have marked as very good,
	good_indexs = []
	good_ids = []
	for i,id_ in enumerate(uni_ids):
		if gt[id_]["Good?"] == 1:
			good_ids.append(id_)
			good_indexs.append(i)
	return good_indexs, good_ids

def EarlyFusionofFeatures(audio_feat,video_feat,audio_ids,video_ids):
	# This function performs early fusion of the features, and then returns the result
	# Let's first create a version of this where have to make sure that we have the same numver of 
	# features
	if len(audio_ids) != len(video_ids):
		print "We don't have audio and video for every video"
		sys.exit(0)

	# Now let's create the video shapes
	video_feat_shape = video_feat.shape
	audio_feat_shape = audio_feat.shape
	num_points = len(audio_ids) # same as video ids based on above check
	feats = np.zeros((num_points,video_feat_shape[1]+audio_feat_shape[1]))
	resorted_video_feats = np.zeros((num_points,video_feat_shape[1]))
	final_ids = []
	for i,audio_id in enumerate(audio_ids):
		final_ids.append(audio_id)
		vid_idx = video_ids.index(audio_id)
		feats[i,:] = np.hstack((video_feat[vid_idx,:],audio_feat[i,:]))
		resorted_video_feats[i,:] = video_feat[vid_idx,:]
	return feats,final_ids, resorted_video_feats


if __name__ == "__main__":
	# Main function runs classification
	audio_dir = "/home/jellis/Project_Data/audio_features"
	gt_dir = "/home/jellis/Project_Data/ground_truth"
	video_dir = "/home/jellis/Project_Data/core_extraction"
	

	# Extrac the features and ids
	video_feats, video_uni_ids = CollectVideoFeats_per_face(video_dir,10000)

	# Let's just do vidoe classification here
	gt = GetGroundTruth(gt_dir)
	# Normalize across all total values of vidual features
	big_ass_feat_vec = video_feats[0]
	for feat in video_feats[1:]:
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

	# Now go through the vector of values and recreate the new one
	norm_video_feats_list = []
	for feat in video_feats:
		norm_feat = np.zeros(feat.shape)
		for z in range(feat.shape[0]):
			norm_feat[z,:] = (feat[z,:] - total_mean) / total_std
		norm_video_feats_list.append(norm_feat)

	# Now let's get the arrays for the labels
	raw_binary_gt, raw_3way_gt = CreateGTArrays(gt,video_uni_ids)

	# Now let's start the tests
	C_arr = 2 ** np.arange(2,7,dtype=float)
	gamma_arr = 2 ** np.arange(-8,-3,dtype=float)
	test_nums = 10

	max_acc = 0
	max_C = 0
	max_gamma = 0

	print "Starting to run the classification tests"
	for i in range(len(C_arr)):
		for j in range(len(gamma_arr)):
			acc_vec = np.zeros(test_nums)
			for k in range(test_nums):
				print "Processing test %d for C=%f and gamma=%f" % (k,C_arr[i],gamma_arr[j])
				
				##### THIS IS SINGLE CLASS CLASSIFICATION ########
				# Seperate the Training and Testing
				train,train_l,test,test_l = SepTrainandTest2(norm_video_feats_list,raw_binary_gt,0.8)

				# Now train the SVM
				svm_clf = trainSVM(train,train_l,C_arr[i],"rbf",gamma_arr[j])
				# Now test the values
				pred_labels,acc = testSVM_max_vote(svm_clf,test,test_l)
				acc_vec[k] = acc

				# Check to see if this is the best configuration
			if np.mean(acc_vec) > max_acc:
				max_acc = np.mean(acc_vec)
				max_C = C_arr[i]
				max_gamma = gamma_arr[j]

			print "The Mean Acc for C=%f and gamma=%f is %f" % (C_arr[i],gamma_arr[j],np.mean(acc_vec))
			#print acc_vec
			#print pred_labels
			#print test_l
			#raw_input("Press Enter")
	print "The max accuracy is: ", max_acc
	print "The best C is: ", max_C
	print "The best gamma is: ", max_gamma

	quit()


	#############NOT USING THIS RIGHT NOW##############

	audio_feats,audio_uni_ids = CollectAudioFeats(audio_dir)

	fused_feats, uni_ids, video_feats = EarlyFusionofFeatures(audio_feats,video_feats,video_uni_ids,audio_uni_ids)
	gt = GetGroundTruth(gt_dir)
	# Test uni_ids
	uni_tests = uni_ids
	# Find the good indices for the np array
	good_indices,uni_tests = GetGoodVideos(gt,uni_tests)

	# Now check the audio feats from the ones that we actually have
	curr_audio_feats = audio_feats[good_indices,:]
	curr_video_feats = video_feats[good_indices,:]
	curr_feats = fused_feats[good_indices,:]

	norm_audio_feats = FeatureNormalization(curr_audio_feats)
	norm_video_feats = FeatureNormalization(curr_video_feats)
	norm_feats = FeatureNormalization(curr_feats)


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
	C_arr = 2 ** np.arange(1,7,dtype=float)
	gamma_arr = 2 ** np.arange(-14,-8,dtype=float)
	test_nums = 100

	max_acc = 0
	max_C = 0
	max_gamma = 0

	print "Starting to run the classification tests"
	for i in range(len(C_arr)):
		for j in range(len(gamma_arr)):
			acc_vec = np.zeros(test_nums)
			for k in range(test_nums):

				
				##### THIS IS SINGLE CLASS CLASSIFICATION ########
				# Seperate the Training and Testing
				train,train_l,test,test_l = SepTrainandTest(norm_video_feats,raw_3way_gt,0.8)

				# Now train the SVM
				svm_clf = trainSVM(train,train_l,C_arr[i],"rbf",gamma_arr[j])

				# Now test the values
				pred_labels,acc = testSVM_max_vote(svm_clf,test,test_l)
				acc_vec[k] = acc
				

				'''
				#4.0 = C_Auido
				#.00024 - gamma_audio
				
				######### Let's do Multi-Class Classificaiton #######
				train,train_l,test,test_l = SepTrainandTest(norm_feats,raw_binary_gt,0.7)
				# Seperate the audio and video train features
				video_train = train[:,0:video_feats.shape[1]]
				audio_train = train[:,video_feats.shape[1]+1:]
				video_test = test[:,0:video_feats.shape[1]]
				audio_test = test[:,video_feats.shape[1]+1:]


				audio_svm_clf = trainSVM(audio_train,train_l,1.0,"rbf",.000244,True)
				video_svm_clf = trainSVM(video_train,train_l,16.0,"rbf",.000244,True)
				
				# Get the probability outputs of each of these values for rbf svm
				audio_train_probs = testSVM(audio_svm_clf,audio_train,train_l,True)
				video_train_probs = testSVM(video_svm_clf,video_train,train_l,True)
				train_probs = np.hstack((audio_train_probs,video_train_probs))

				# Now train our classifier using the output probabilities
				prob_svm_clf = trainSVM(train_probs,train_l,C_arr[j],"linear")

				# Train the late fusion linear svm
				audio_test_probs = testSVM(audio_svm_clf,audio_test,test_l,True)
				video_test_probs = testSVM(video_svm_clf,video_test,test_l,True)
				test_probs = np.hstack((audio_test_probs,video_test_probs))

				pred_labels, acc = testSVM(prob_svm_clf,test_probs,test_l)
				acc_vec[k] = acc
				'''

			# Check to see if this is the best configuration
			if np.mean(acc_vec) > max_acc:
				max_acc = np.mean(acc_vec)
				max_C = C_arr[i]
				max_gamma = gamma_arr[j]

			print "The Mean Acc for C=%f and gamma=%f is %f" % (C_arr[i],gamma_arr[j],np.mean(acc_vec))
			#print acc_vec
			#print pred_labels
			#print test_l
			#raw_input("Press Enter")
	print "The max accuracy is: ", max_acc
	print "The best C is: ", max_C
	print "The best gamma is: ", max_gamma