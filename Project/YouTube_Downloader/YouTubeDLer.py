#!/usr/bin/env python
# Created by Joe Ellis and Jessica Ouyang
# Columbia DVMM and NLP Lab Groups
# Logistic Progression -- CUNY NLP/ML/Web Technologies

### Necessary python libraries ###
import os, sys, getopt
import subprocess as sub
from gdata.youtube import service
import json
from bs4 import BeautifulSoup

# Class for interacting with youtube
class YouTubeUtils():
	
	def __init__(self, path_to_youtubedl, download_dir):
		
		#These set up the class variables of where the downloader is 
		self.path_to_youtubedl = path_to_youtubedl
		self.download_dir = download_dir

		# Set up the youtube client, let's see if we can do it without log in
		self.client = service.YouTubeService()

		return

	def DownloadVideo(self,url):
		# This downloads the video
		execpath = self.path_to_youtubedl

		# Now create the output directory for this video
		if self.download_dir[-1] == "/":
			download_dir = self.download_dir
		else:
			download_dir = self.download_dir + "/"

		# This options is what we want to use the 
		o_option = "'%s%s'" % (download_dir,"%(title)s.%(ext)s")

		output = sub.Popen(execpath + " -o " 
									+ o_option 
									+ " --write-info-json " 
									+ url, 
									shell=True)
		output.communicate()
		print "Just downloaded the video and info at %s" % url
		return

	def GetCommentsforVideo(self, vid_id):
		# This function gets the comments for a given youtube video
		# The vid_id is the number pattern that appears in the video webpage
		comment_feed = self.client.GetYouTubeVideoCommentFeed(video_id=vid_id)
		video_comments = []
		while comment_feed is not None:
			for comment in comment_feed.entry:
				video_comments.append(comment)
			next_link = comment_feed.GetNextLink()
			if next_link is None:
				comment_feed = None
			else:
				comment_feed = self.client.GetYouTubeVideoCommentFeed(next_link.href)

		# Now let's extract the meaningful portion of the comments, like their
		# name and their comment
		names_and_comments = []
		for video_comment in video_comments:
			soup = BeautifulSoup(str(video_comment).decode("utf-8"))
			name = soup.find("ns0:name")
			content = soup.find("ns0:content")
			if name != None:
				names_and_comments.append((name.string,content.string))
		
		return names_and_comments




### The Main run portion of the code ###
if __name__ == "__main__":
	ydl = YouTubeUtils("./YouTube_Downloader/youtube-dl", "YouTubeVideos")
	#ydl.DownloadVideo("http://www.youtube.com/watch?v=lQGDqH6rHII")
	ydl.GetCommentsforVideo("lQGDqH6rHII")

