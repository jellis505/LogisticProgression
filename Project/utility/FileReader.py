#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# News Rover System
# Digital Video & Multimedia Lab
# Columbia University

import os, json, wikiapi
import datetime
from bs4 import BeautifulSoup

def ReplaceExt(srcname, newext):
    filename, fileext = os.path.splitext(srcname)
    return filename + newext

def read_char_times(segmentfile):
    triple_char_times = []
    with open(segmentfile) as f:
        lines = f.readlines()
            
        # first line
        line = lines[0]
        timestring = line[0:8]
        time_ = timestring.split(':')
        dur = int(time_[0])*3600 + int(time_[1])*60 + int(time_[2])
        triple_char_times.append( (0,dur) )
            
        # remaining lines
        for line in lines:
            timestring = line[0:8]
            time_ = timestring.split(':')
            begin = int(time_[0])*3600 + int(time_[1])*60 + int(time_[2])
                
            timestring = line[14:21]
            time_ = timestring.split(':')
            dur = int(time_[0])*3600 + int(time_[1])*60 + int(time_[2])
            triple_char_times.append( (begin,dur) )
        
    return triple_char_times

def read_nodes_file(descfile, type_of_node):
    # open the file for the nodes
    f = open(descfile, 'r')
    lines = f.readlines()
  
    # create the list to hold all the variables
    nodes = []

    # iterate through the lines
    for line in lines:
        if line[0] == '#':
	        print 'Skipping Comment'
        else:
            # find start time
            findcomma = line.find(',')
            starttime = line[0:findcomma]
            line = line[findcomma+1:]

            # find duration 
            findcomma = line.find(',')
            durtime = line[0:findcomma]
            line = line[findcomma+1:]

            # get name
            length = len(line)
            name = line[0:length-1]

            if type_of_node == 'video':
                startframe = float(starttime)
                durframes = float(durtime)
                start_sec = startframe/29.97 #TODO: change to get_frame_rate
                dur_sec = durframes/29.97 #TODO: change to get_frame_rate
                node = (start_sec,dur_sec)
            else:
                node = (float(starttime),float(durtime),name)
            nodes.append(node)

    return nodes
 
def read_unique_names(uniquenamefile):
    # open file for the uniquenamefile
    f = open(uniquenamefile,'r')
  
    lines = f.readlines()
  
    # read unique name file
    uniquenames = []
  
    # create iterator
    unique_iter = iter(lines)
  
    for line in unique_iter:
        # get all names
        names = []
        findcolon = line.find(':')
        length = len(line)
        line = line[findcolon+2:length-1]
        names = line.split(',')
    
        # get all CC times
        line = next(unique_iter)
        cctimes = []
        findcolon = line.find(':')
        length = len(line)
        line = line[findcolon+2:length-1]
        cctimes = line.split(',')

        # get all OCR times
        line = next(unique_iter)
        ocr_times = []
        findcolon = line.find(':')
        length = len(line)
        if length == 6:
            ocr_times = ['']
        else:
            line = line[findcolon+2:length-1]
            numbers = line.split(',')
            numbers_iter = iter(numbers)
            for number in numbers_iter:
                starttime = number
                durtime = next(numbers_iter)
                startframe = float(starttime)
                durframes = float(durtime)
                start_sec = startframe/29.97 #TODO: change to get_frame_rate
                dur_sec = durframes/29.97 #TODO: change to get_frame_rate
                #start_sec = startframe/59.94 #TODO: change to get_frame_rate
                #dur_sec = durframes/59.94 #TODO: change to get_frame_rate
                start_dur = (start_sec,dur_sec)
                ocr_times.append(start_dur)
    
        # combine all of these portions into one unique name
        uniquenames.append((names,cctimes,ocr_times))

    return uniquenames
 
def read_diafile(diarizationfile):
    f = open(diarizationfile,'r')

    lines = f.readlines()
    lines = [line.rstrip('\r\n') for line in lines]
    lines = [line.rstrip('\n') for line in lines]
    nodes = []

    for line in lines:
        if line[0:4] != 'SPKR':
            # We need to get the beginning, end and the cluster of these segements
            first = line.find('1')
            second = line.find('<')
            parts = line[first+2:second-1].split(' ')
            start = float(parts[0])
            duration = float(parts[1])
            second = line.rfind('<')
            first = line[0:second-1].rfind('>')
            speaker_clust = line[first+2:second-1]
            nodes.append((start,duration,speaker_clust))

    f.close()
    
    return nodes
    
def read_segfile(segfile):
    f = open(segfile,'r')
    
    lines = f.readlines();
    lines = [line.rstrip('\r\n') for line in lines]
    lines = [line.rstrip('\n') for line in lines]
    nodes = []
    
    for line in lines:
        if line[0:4] == 'SPEA':
            # We need to get the beginning, end and the cluster of these segments
            first = line.find('5')
            second = line.find('<')
            parts = line[first+2:second-1].split(' ')
            start = float(parts[0])
            duration = float(parts[1])
            second = line.rfind('<')
            first = line[0:second-1].rfind('>')
            speaker_clust = line[first+2:second-1]
            nodes.append((start,duration,speaker_clust))

    return nodes
     
def output_clustered_speech(nodes,matches,filename):
    # find which names are mentioned the most within each speaker name
    # this portion matches the names with the speaker clusters

    f = open(filename,'w')

    for node in nodes:
        start = node[0]
        end = node[1]
        speakercluster = node[2]
        for match in matches:
            if match[0] == speakercluster:
                names = match[1]
                break
        write_string = ",".join([str(start),str(end),speakercluster,names]) + '\n'
        f.write(write_string)

    f.close()

def ReadTranscriptFile(filepath):
    with open(filepath,'r') as f:
        lines = f.readlines()
        lines = [line.rstrip('\r\n') for line in lines]
        lines = [line.rstrip('\n') for line in lines]
    
    # Create tuples of the word transcript times
    frame_and_word = [line.split('\t') for line in lines]
    
    # Get ms time for each word
    ms_and_word = [(float(frame)/29.97,word) for frame,word in frame_and_word]
    
    # Now let's find the placement of the >> words
    char_times = [ms for (ms,word) in ms_and_word if word == '>>']
    
    spkr_times = []
    num_times = len(char_times)
    
    if len(char_times) == 0:
        spkr_times.append((0,ms_and_word[-1][0]))
    
    for i,char_time in enumerate(char_times):
        if i == 0:
            spkr_times.append((0,char_time))
        elif i+1 < num_times:
            spkr_times.append((spkr_times[-1][1],char_time))
        else:
            spkr_times.append((spkr_times[-1][1],ms_and_word[-1][0]))
    
    #print char_times
    #print spkr_times
    return ms_and_word,char_times,spkr_times 
        
def GetValidSegments(rootpath):
    video_dir = os.path.join(rootpath,"videos")
    # Get all of the files in the os directory
    files = os.listdir(video_dir)[0:]
    valid_segs_w_ext = [file for file in files if ((not file.find('invaild') + 1) and bool(file.find('.mp4') + 1) and (not file.find('000') + 1))]
    valid_segs = [ReplaceExt(seg,"") for seg in valid_segs_w_ext] 
    
    return valid_segs

def ReadSegmentFrames(file):
    with open(file,'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
        line_vals = [line.split('\t') for line in lines]
        
    segment_frames = []
    for line_val in line_vals:
        seg_string = "%03d" % int(line_val[0])
        start = int(line_val[1])
        end = int(line_val[2])
        segment_frames.append((seg_string,start,end))
    
    segment_times = [(seg,start/29.97,end/29.97) for (seg,start,end) in segment_frames]
    
    return segment_frames,segment_times

def GetProgramNameandDate(rootpath):
    # remove the last \
    if rootpath[-1] == '/':
        rootpath = rootpath[:-1]
    program_and_time = rootpath[rootpath.rfind('/')+1:]
    
    # Now get the program
    time_point = program_and_time.rfind('2013' or '2012' or '2014')
    DIG_point = program_and_time.find('_DIG_')
    if DIG_point == -1:
        program = program_and_time[:time_point-1].replace('_',' ')
    else:
        program = program_and_time[:DIG_point].replace('_',' ')
    
    # Now let's get the times
    date = program_and_time[time_point:time_point+8]
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    
    # airtime here
    airtime = program_and_time[time_point+9:]
    
    return program,year,month,day,airtime
"""
def ReturnWikipediaImage(query_name):
    # Initialize the object
    wiki = wikiapi.wikiApi()
    results = wiki.find(query_name)
    
    # Check to see if we got results
    if len(results) > 0:
"""        

def GetDate(days_removed=None):
    # This function returns the month, day and year
    if (days_removed == None) or (days_removed == 0):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
    else:
        yesterday = datetime.datetime.now() - datetime.timedelta(days_removed)
        year = yesterday.year
        month = yesterday.month
        day = yesterday.day
    return day,month,year
    
def ReadArticlesforTopic(topic_file_path):
    # make the soup
    soup = BeautifulSoup(open(topic_file_path,"r").read())
    articles = soup.articles.find_all("newsarticle")

    # This gets the title and description together in a string 
    content = [(article.title.string,article.description.string) for article in articles]
    
    # this gets the title and descriptions seperately not used
    #titles = [article.title.string for article in articles]
    #descriptions = [article.description.string for article in articles]
    
    return content

def GetFileOnly(filepath):
    if "/" in filepath:
        pos = filepath.rfind("/")
        file_ = filepath[pos+1:]
    else:
        file_ = filepath
    return file_

def ConnectSpkrSegs(person_segs):
    # Returns the longest possible consecutive speech segments
    segments = []
    last_speaker = person_segs[0][2]
    start_of_seg = 0
    for i,(start,end,speaker) in enumerate(person_segs[1:]):
        if speaker != last_speaker:
            spkr_seg = (start_of_seg,(person_segs[i][0]+person_segs[i][1])-start_of_seg,last_speaker)
            segments.append(spkr_seg)
            start_of_seg = start
            last_speaker = speaker

    spkr_seg = (start_of_seg,person_segs[-1][0]+person_segs[-1][1]-start_of_seg,last_speaker)
    segments.append(spkr_seg)
    return segments 

def ReadFaceFile(filepath):
    with open(filepath,"r") as f:
        raw_lines = f.readlines()
        lines = [line.rstrip("\n") for line in raw_lines]
        faces = []
        for line in lines:
            raw_parts = line.split("\t")
            parts = [int(part) for part in raw_parts]
            faces.append(parts)

    return faces


    
if __name__ == "__main__":
    # This is only used to debug the reader functionality of the function above
    file = '/ptvn/tmp/segTest2/ABC_World_News_Now_DIG_20130823_0236/segments.txt'
    a,b = ReadSegmentFrames(file)
    print a
    print b
    
    

    
    






