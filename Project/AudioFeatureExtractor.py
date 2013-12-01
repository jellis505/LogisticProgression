#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Joe Ellis
# Digital Video & Multimedia Lab
# Logistic Progression

#### Import Libraries ######
import os, sys, getopt
import subprocess as sub
import shutil
sys.path.append("utility")
import FileReader as reader

##### Global Variables #######

class AudioExtractor():
	def __init__(self, wav_file):
		self.video_file = video_file
