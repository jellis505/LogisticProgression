#!/usr/bin/env python
#Created by Joe Ellis
# Logistic Progression 

##### Libraries ##########
# These are the import libraries
import os, sys
import cv2
import numpy as np 
from skimage.feature import local_binary_pattern
##########################


########## Global Variables ########
# These are the global variables we will use here
global face_cascade
face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

global skin_threshs
skin_thresh_lower = np.array([0,133,77])
skin_thresh_upper = np.array([255,173,127])
####################################


def DetectFacesandOutput(frame,frame_num,output_dir):
	# Passes in the frame in numpy format
	#transform the image to gray scale 
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	
	for i,(x,y,w,h) in enumerate(faces):
		roi_face = frame[y:y+h, x:x+w]
		roi_gray = gray[y:y+h, x:x+w]
		# Now that we have the face let's detect the faces and then output them to the directory
		image_name = "%05d_%02d.png" % (frame_num,i)
		output_path = os.path.join(output_dir,image_name)
		cv2.imwrite(output_path,roi_face)

		# Let's resize the roi_face and then calculate the LBP features
		desired_size = 100
		x_size, y_size, depth = roi_face.shape
		x_ratio = desired_size/float(x_size)
		y_ratio = desired_size/float(y_size)
		new_image = cv2.resize(gray,(desired_size,desired_size))

	return

def ExtractLBPFeatures(img):
	# This function extracts LBP features from a given image
	radius = 3
	n_points = 8 * radius
	lbp_feature = local_binary_pattern(image,n_points,radius)

	return lbp_feature

def GetSkinMask(img):
	# This function gets the skin mask of an image, and then the goal is to 
	# track the movement of the head and hands

	ksize = [15,15]
	new_img = cv2.cvtColor(img,cv2.COLOR_RGB2YCR_CB)
	blurred_img = cv2.GaussianBlur(img,ksize,3,3)

	# This section does the calculation of the numpy array
	skin_mask = cv2.inRange(blurred_img,skin_thresh_lower,skin_thresh_upper)

	return skin_mask

if __name__ == "__main__":
	# This program will detect the faces and save them to a file for the given videos that we have
	video_file = sys.argv[1]
	output_dir = sys.argv[2]

	# This is the opencv video capture object
	cap = cv2.VideoCapture(video_file)

	# This returns the frame of the video
	while(1):

		# This gets the frame and is numpy array, ret is false if there is no more video
		ret, frame = cap.read()

		# We want to downsample so that we only process every second, or 30 frames
		if ret:

			frame_num = cap.get(1)
			# We will downsample to only process every 30 seconds
			if frame_num % 30 == 0:
				DetectFacesandOutput(frame,frame_num,output_dir)

			if frame_num % 5 == 0:
				skin_mask = GetSkinMask

		else:
			print "Done Processing the video"
			break
