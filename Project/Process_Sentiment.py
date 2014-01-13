#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Import libraries
import os, sys
import subprocess as sub

# global variables
# These are the windows settings
"""
g_orig_video_dir = 'E:\Youtube_data_package\data_package\data\Videos'
g_new_video_dir = 'E:\Youtube_data_package\data_package\data\cut_videos'
g_orig_audio_dir = 'E:\Youtube_data_package\data_package\data\Audio'
g_new_audio_dir = 'E:\Youtube_data_package\data_package\data\cut_audios'
g_label_file = 'label_file.csv'
"""

## Global Variables for linux environment
g_orig_video_dir = '/home/jellis/YouTubeProject/Youtube_data_package/data_package/data/Videos'
g_new_video_dir = '/home/jellis/YouTubeProject/Youtube_data_package/data_package/data/cut_videos'
g_orig_audio_dir = '/home/jellis/YouTubeProject/Youtube_data_package/data_package/data/Audio'
g_new_audio_dir = '/home/jellis/YouTubeProject/Youtube_data_package/data_package/data/cut_audio'
g_label_file = '/home/jellis/YouTubeProject/Youtube_data_package/data_package/annotations/sentiment/label_file.csv'
g_sentiment_file = '/home/jellis/YouTubeProject/Youtube_data_package/data_package/annotations/sentiment/sentimentAnnotations.csv'


if __name__ == "__main__":
    # <codecell>

    # Now read in the sentiment annotations files
    with open(g_sentiment_file, 'r') as f:
        raw_lines = f.readlines()
        lines = [line.rstrip("\n").rstrip("\r\n") for line in raw_lines]
        parts = [line.split(",") for line in lines]

    # <codecell>

    # Now get each part into a dictionary
    dict_names = parts[0]
    print dict_names
    utterances = []
    for part in parts[1:]:
        part_dict = dict()
        for p,name in zip(part,dict_names):
            part_dict[name] = float(p)
        utterances.append(part_dict)

    # <codecell>

    # Now get the files in video files
    orig_videos = [os.path.join(g_orig_video_dir,o) for o in os.listdir(g_orig_video_dir) if '.db' not in o]
    orig_wavs = [os.path.join(g_orig_audio_dir,o) for o in os.listdir(g_orig_audio_dir) if '.db' not in o]

    # <codecell>

    # Now that we have the utterances in list, we want to get our ffmpeg commands for each utterance
    ffmpeg_commands = []
    wav_commands = []

    # Get the ffmpeg commands we need to get the section of videos and utterances that we want
    for video in orig_videos:
        vid_index = int(video[video.rfind("o")+1:video.find("(")])
        
        # Now that we have the video index, let's find all of the utterances within that video
        for utterance in utterances:
            if vid_index == utterance['video']:
                if utterance['start time'] == -1:
                    utterance['start time'] = 0
                new_video_file_name = os.path.join(g_new_video_dir,str(vid_index) + "_" + str(utterance['start time']) + "_" + str(utterance['end time']) + ".mp4")
                duration = utterance['end time'] - utterance['start time']
                command = 'ffmpeg' + " -i '" + video + "' -ss " + str(utterance['start time']) + " -t " + str(duration) + " -y '" + new_video_file_name + "'"
                ffmpeg_commands.append(command)

    # Now let's get to the wav file values 
    for video in orig_wavs:
        vid_index = int(video[video.rfind("o")+1:video.find("(")])
        
        # Now that we have the video index, let's find all of the utterances within that video
        for utterance in utterances:
            if vid_index == utterance['video']:
                if utterance['start time'] == -1:
                    utterance['start time'] = 0
                new_video_file_name = os.path.join(g_new_audio_dir,str(vid_index) + "_" + str(utterance['start time']) + "_" + str(utterance['end time']) + ".wav")
                duration = utterance['end time'] - utterance['start time']
                command = 'ffmpeg' + " -i '" + video + "' -ss " + str(utterance['start time']) + " -t " + str(duration) + " -y '" + new_video_file_name + "'"
                wav_commands.append(command)
         

    # <codecell>

    # Now let's get the labels for each of the videos and utterances
    # then we can use these to figure out how are values get good.
    with open(g_label_file,"w") as f:
        for utterance in utterances:
            video_file = str(utterance['video']) + "_" + str(utterance['start time']) + "_" + str(utterance['end time']) + ".mp4"
            vote = str(utterance['Majority vote'])
            f.write(video_file + "," + vote + "\n")

    # <codecell>

    # Now that we have written the label file here, let's now get the commands
    # Now let's run through the ffmpeg commands that we need
    for ffmpeg_command in ffmpeg_commands:
        output = sub.Popen(ffmpeg_command, shell=True)
        output.communicate()

    for wav_command in wav_commands:
        output = sub.Popen(wav_command,shell=True)
        output.communicate()


