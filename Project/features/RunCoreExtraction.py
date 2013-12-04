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
##########################

global execpath
execpath = "/ptvn/bin/CoreExtraction"


def run(argv):
	# This function runs CoreExtraction for an entire segmented video
	# Now let's parse the arguements
	try:
		opts, args = getopt.getopt(argv,'hi:o:')
	except getopt.GetoptError:
		print "You did something wrong"
		sys.exit(0)

	# Parse the arguements in
	video_dir = None
	output_dir = None
	for opt, arg in opts:
		if opt in ('-h'):
			print "HELP!"
			sys.exit(0)
		elif opt in ('-i'):
			video_dir = arg
		elif opt in ('-o'):
			output_dir = arg

	# Check to make sure that the output are sufficient
	if not (video_dir and output_dir):
		print "You did not include either the video_dir or the output_dir"
		sys.exit(0)

	# Check to see if the executable function is installed on this machine
	if not os.path.exists(execpath):
		print "You need the CoreExtraction executable, talk to the News Rover team at Columbia University"
		sys.exit(0)

	# Let's get all of the videos here that are in the directory
	files = os.listdir(video_dir)
	videos = [file_ for file_ in files if ".mp4" in file_]
	video_paths = [os.path.join(video_dir,video) for video in videos]

	# Now let's loop through the videos and process them
	
	# DEBUG 
	print video_paths

	for video_path in video_paths:
		# Create the output files
		file_only = reader.GetFileOnly(video_path)
		file_no_ext = reader.ReplaceExt(file_only,"")
		output_path = os.path.join(output_dir,file_no_ext)
		if not os.path.exists(output_path):
			os.makedirs(output_path)
		command = execpath  + " -i " + video_path \
						 	+ " -o " + output_path \
						 	+ " -fs " + str(15) 
		print command
		output = sub.Popen(command,shell=True)
		output.communicate()
		
		# Now remove the extra directories that we don't need for this
		# project
		ocr_dir = os.path.join(output_path,"ocr")
		face_dir = os.path.join(output_path,"faces")
		shutil.rmtree(ocr_dir)
		shutil.rmtree(face_dir)
	return


if __name__ == "__main__":
	run(sys.argv[1:])
