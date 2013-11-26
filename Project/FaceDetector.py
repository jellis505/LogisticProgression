#!/usr/bin/env python
#Created by Joe Ellis
# Logistic Progression 

##### Libraries ##########
# These are the import libraries
import os, sys, math
import cv2
import numpy as np 
from skimage.feature import local_binary_pattern
##########################


########## Global Variables ########
# These are the global variables we will use here
global face_cascade
face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')

global skin_threshs
g_skin_thresh_lower = np.array([0,133,77])
g_skin_thresh_upper = np.array([255,173,127])
####################################


# Modified from bytefish face alignement code
def CropandAlignFace(image,eye_left,eye_right,offset_pct,dest_sz):
	# calculate offsets in original image
  	offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
 	offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
 	# get the direction
  	eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  	# calc rotation angle in radians
  	rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  	print rotation
	dist = math.sqrt((eye_left[0]-eye_right[0])*(eye_left[0]-eye_right[0])+(eye_left[1]-eye_right[1])*(eye_left[1]-eye_right[1]))

	# reference eye-width, or how far apart they actually have to be
	# calculate the reference eye-width
  	reference = dest_sz[0] - 2.0*offset_h

  	# This is the scale factor we have to enlarge the picture by
  	# scale factor
  	scale = float(dist)/float(reference)

  	# Now that we have the scale factor, let's rotate the image and perform an affine warp on it
  	center = eye_left
  	angle = -rotation
  	nx,ny = x,y = center
	sx=sy=1.0
	cosine = math.cos(angle)
	sine = math.sin(angle)
	a = cosine/sx
	b = sine/sx
	c = x-nx*a-ny*b
	d = -sine/sy
	e = cosine/sy
	f = y-nx*d-ny*e

	# Affine transform matrix
	M = np.array([[a,b,c],[d,e,f]])
	print M

	warped_image = cv2.warpAffine(image,M,(image.shape[0],image.shape[1]))
	
	# Debug Purposes
	#cv2.imshow("warp_image",warped_image)
	#cv2.waitKey(0)
	# crop the rotated image
  	crop_xy = (eye_left[1] - scale*offset_h, eye_left[0] - scale*offset_v)
 	crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
 	print warped_image.shape
 	warped_image = warped_image[int(crop_xy[0]):int(crop_xy[0]+crop_size[0]), int(crop_xy[1]):int(crop_xy[1]+crop_size[1])]
 	
 	# Debug Purposes
 	#cv2.imshow("warp_images",warped_image)
 	#cv2.waitKey(0)
 	#return warped_image
 	print crop_xy
 	print crop_size 
 	print warped_image.shape
 	return cv2.resize(warped_image,dest_sz)


def DetectFacesandOutput(frame,frame_num,output_dir):
	# Passes in the frame in numpy format
	#transform the image to gray scale 
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	
	# Assume square faces
	desired_size = 100

	# List of vector means and standard deviations
	means = []
	stds = []

	for i,(x,y,w,h) in enumerate(faces):
		roi_face = frame[y:y+h, x:x+w]
		roi_gray = gray[y:y+h, x:x+w]

		# Here let's find the eye points using the cascade classifier
		eyes = eye_cascade.detectMultiScale(roi_gray)
		if len(eyes) == 2:
			# Let's rotate the image so that they all appear the same
			if eyes[0][0] < eyes[1][0]:
				right_eye = (eyes[0][0]+x+int(eyes[0][2]/float(2)),eyes[0][1]+y+int(eyes[0][3]/float(2)))
				left_eye = (eyes[1][0]+x+int(eyes[1][2]/float(2)),eyes[1][1]+y+int(eyes[1][3]/float(2)))
			else:
				right_eye = (eyes[1][0]+x+int(eyes[1][2]/float(2)),eyes[1][1]+y+int(eyes[1][3]/float(2)))
				left_eye = (eyes[0][0]+x+int(eyes[0][2]/float(2)),eyes[0][1]+y+int(eyes[0][3]/float(2)))

			# Here we will crop the face to get the faces_aligned based on the news video
			cropped_face = CropandAlignFace(frame,right_eye,left_eye,(0.2,0.2),(desired_size,desired_size))

			# Now that we have the face let's detect the faces and then output them to the directory
			image_name = "%05d_%02d.png" % (frame_num,i)
			output_path = os.path.join(output_dir,image_name)
			#cv2.imwrite(output_path,roi_face)

			# Let's resize the roi_face and then calculate the LBP features
			x_size, y_size, depth = roi_face.shape
			x_ratio = desired_size/float(x_size)
			y_ratio = desired_size/float(y_size)
			new_image = cv2.resize(gray,(desired_size,desired_size))

			# To get an accurate skin detector let's take a look at the middle fo the frame and the skin colors
			#roi_skin_face = frame[y+(0.2*h):y+(0.8*h), x+(0.2*w): x+(0.8*w)]
			roi_skin_face = cropped_face
			cv2.imwrite(output_path,roi_skin_face)
			roi_skin_face = cv2.cvtColor(roi_skin_face,cv2.COLOR_BGR2YCR_CB)

			# Get the means and standard deviation
			means.append(np.array([np.mean(roi_skin_face[:,:,0]),np.mean(roi_skin_face[:,:,1]),np.mean(roi_skin_face[:,:,2])]))
			stds.append(np.array([np.std(roi_skin_face[:,:,0]),np.std(roi_skin_face[:,:,1]),np.std(roi_skin_face[:,:,2])]))

	if len(means) == 1:
		skin_thresh_upper_used = means[0] + 1.5*stds[0]
		skin_thresh_lower_used = means[0] - 1.5*stds[0]
		return skin_thresh_lower_used, skin_thresh_upper_used

	# This section needs to be changed, as it assumes that we still only have one detected face
	elif len(means) > 1:
		skin_thresh_upper_used = means[0] + 1.5*stds[0]
		skin_thresh_lower_used = means[0] - 1.5*stds[0]
		return skin_thresh_lower_used, skin_thresh_upper_used
	
	else:
		return None, None

def ExtractLBPFeatures(img):
	# This function extracts LBP features from a given image
	radius = 3
	n_points = 8 * radius
	lbp_feature = local_binary_pattern(image,n_points,radius)

	return lbp_feature

def GetSkinMask(img,frame_num,output_dir, skin_thresh_lower_used=None, skin_thresh_upper_used=None):
	# This function gets the skin mask of an image, and then the goal is to 
	# track the movement of the head and hands
	if skin_thresh_lower_used == None:
		skin_thresh_lower_used = g_skin_thresh_lower
		skin_thresh_upper_used = g_skin_thresh_upper

	ksize = (15,15)
	#new_img = img
	new_img = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
	blurred_img = cv2.GaussianBlur(new_img,ksize,3,3)

	# This section does the calculation of the numpy array
	skin_mask = cv2.inRange(blurred_img,skin_thresh_lower_used,skin_thresh_upper_used)

	# Now let's get the skin contours here.
	skin_contours, _ = cv2.findContours(skin_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	contour_img = np.zeros(skin_mask.shape)

	for i,c in enumerate(skin_contours):
		if cv2.contourArea(c) > 500 and cv2.contourArea(c) < 10000:
			cv2.drawContours(contour_img,skin_contours,i,255,-1)

	skin_mask_name = image_name = "skin_mask_%05d.png" % (frame_num)
	skin_mask_file = os.path.join(output_dir,skin_mask_name)
	cv2.imwrite(skin_mask_file,contour_img)



	return skin_mask

if __name__ == "__main__":
	####This section is for debug purposes only#####
	#image_file = sys.argv[1]
	#frame = cv2.imread(image_file)
	#skin_thresh_lower_used, skin_thresh_upper_used = DetectFacesandOutput(frame,10,'test_pic')
	#GetSkinMask(frame,10,'test_pic',skin_thresh_lower_used,skin_thresh_upper_used)
	#quit()
	####

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
				skin_thresh_lower_used, skin_thresh_upper_used = DetectFacesandOutput(frame,frame_num,output_dir)
				GetSkinMask(frame,frame_num,output_dir,skin_thresh_lower_used,skin_thresh_upper_used)

		else:
			print "Done Processing the video"
			break
