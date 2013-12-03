#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Joe Ellis
# Digital Video & Multimedia Lab
# Logistic Progression

# Import Libraries
import os, sys, getopt
import subprocess as sub
import shutil
sys.path.append("utility")
import FileReader as reader

### Glolbal variables ###
global sadmodelfile
sadmodelfile = 'models/shout.sad'

def shout_vid2wav(videofile,audiofile):
    command = 'ffmpeg -i ' + videofile + \
                    ' -vn -acodec pcm_s16le' + \
                    ' -ar 16000 -ac 1 -f s16le' + \
                    ' -loglevel quiet -y ' + audiofile
    print command
    return_code = sub.call(command,shell=True)

    return return_code

def shout_segment(rawfile,segmentfile):
    if not os.path.exists(sadmodelfile):
        print 'Could not find speech activity detection model for SHoUT at: ' + \
                    os.path.join(os.getcwd(),sadmodelfile)
        sys.exit(1)

    command = 'shout_segment -a '   + rawfile + \
                           ' -ams ' + sadmodelfile + \
                           ' -mo '  + segmentfile
    print command
    return_code = sub.call(command,shell=True)

    return return_code

def shout_cluster(rawfile,segmentfile, diarizationfile):
    command = 'shout_cluster -a '  + rawfile + \
                           ' -mi ' + segmentfile + \
                           ' -mo ' + diarizationfile
    print command
    return_code = sub.call(command,shell=True)

    return return_code

def cut_video(segments,videofile,output_dir,file_id):
	for i,segment in enumerate(segments):
		# Extract the portion of the video into a small video portion
		cut_vid_file = '%s_%03d.mp4' % (file_id,i)
		cut_vid_path = os.path.join(output_dir,cut_vid_file)
		command = 'ffmpeg -y -i ' + videofile + \
					' -ss ' + str(segment[0]) + \
					' -t ' + str(segment[1]) + \
					' ' + cut_vid_path
		print command
		return_code = sub.call(command,shell=True)
		
		# Create Wavfile
		cut_vid_wav_path = reader.ReplaceExt(cut_vid_path,".wav")
		command = 'ffmpeg -y -i ' + cut_vid_path + \
					' ' + cut_vid_wav_path
		print command
		return_code = sub.call(command,shell=True)

	return 

def run(argv):
	# Now let's parse the arguements
	try:
		opts, args = getopt.getopt(argv,'hi:o:w:')
	except getopt.GetoptError:
		print "You did something wrong"
		sys.exit(0)

	video_file = None
	output_folder = None
	wavfile_dir = None
	for opt, arg in opts:
		if opt in ('-h'):
			print "HELP!"
			sys.exit(0)
		elif opt in ('-i'):
			video_file = arg
		elif opt in ('-o'):
			output_folder = arg
		elif opt in ('-w'):
			wavfile_dir = arg

	if not (video_file and output_folder and wavfile_dir):
		print "You need more arguments to run this code"
		sys.exit(0)

	### THIS SECTION OF CODE USES THE SHoUT Toolbox ########
	# Now do the diarization to start us out
	file_id_with_ext = reader.GetFileOnly(video_file)
	file_id = reader.ReplaceExt(file_id_with_ext,"")
	raw_file = file_id + ".raw"
	raw_file = os.path.join(wavfile_dir,raw_file)
	# Perform turning the video into ."raw" audiofile
	return_code = shout_vid2wav(video_file,raw_file)

	if return_code:
		print "We had an issue in: VIDEO TRANSCODING"
		sys.exit(0)

	# Perform segmentation
	seg_file = os.path.join(output_folder,file_id + ".seg")
	return_code = shout_segment(raw_file,seg_file)

	if return_code:
		print "We had an issue in: SEGMENTATION"
		sys.exit(0)

	# Perform Diarization
	dia_file = reader.ReplaceExt(seg_file,".dia")
	return_code = shout_cluster(raw_file,seg_file,dia_file)

	if return_code:
		print "We had an issue in: CLUSTERING"
		sys.exit(0)
	###################################################

	# Now let's parse through the clustering file, and find the speaker times for each video
	person_segs = reader.read_diafile(dia_file)
	
	# Now we need to combine the sections of speech that are concurrent between people
	segments = reader.ConnectSpkrSegs(person_segs)

	# This cuts up the video and outputs it to the desired directory
	# Create a directory to hold all of the videos for this particular youtube program
	output_vid_segs_dir = os.path.join(output_folder,file_id)
	if not os.path.exists(output_vid_segs_dir):
		os.makedirs(output_vid_segs_dir)

	cut_video(segments,video_file,output_vid_segs_dir,file_id)

	# Now we need to output a file that has the time segments available
	output_seg_time_file = os.path.join(output_vid_segs_dir,file_id + ".times")
	with open(output_seg_time_file, "w") as f:
		for i,segment in enumerate(segments):
			output = "%03d,%.2f,%.2f\n" % (i,segment[0],segment[0]+segment[1])
			f.write(output)
			
	# TODO: NEED TO REMOVE THE AUDIO FILES THAT ARE NOT NEEDED BUT CREATED
	os.remove(raw_file)


	print "Finished Processing Video: %s" % file_id

if __name__ == "__main__":
	run(sys.argv[1:]) 