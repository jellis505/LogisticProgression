# Created by Joe Ellis for the Columbia University News Rover System
# 07/15/2013

# Takes in the 3-Char file and 2-Char file and then find the speaking
# times within each segment

import os
import sys
import FileReader

def get_talking_times(triple_char_times,double_char_times):
    # Create a list for the speaker changes in each segment
    speakers = []
    for times in triple_char_times:
        segment_speakers = []
        for char2time in double_char_times:
            if (char2time[0] > times[0]) and char2time[0] < times[0] + times[1]:
                if (char2time[0] + char2time[1]) > times[0]+times[1]:
                    segment_speakers.append( (char2time[0]-times[0],times[1]) )
                else:
                    segment_speakers.append( (char2time[0]-times[0],char2time[1]+char2time[0]-times[0]) )
                    
        # Add the speaker change sections
        if len(segment_speakers) > 0:
            if segment_speakers[0][0] != times[0]:
                segment_speakers.insert(0,(0,segment_speakers[0][0]))
        elif len(segment_speakers) == 0:
            segment_speakers.append((0,times[1]))
        
        # This is the speaker segment section
        speakers.append(segment_speakers)
            
    return speakers

def PrintOutFiles(speakers,outputdir):
    
    # Now we will create the times for each speech segment
    for i, segment in enumerate(speakers):
        outputfile = '%d_speakers.txt' % (i)
        file = os.path.join(outputdir,outputfile)
        with open(file,'w') as f:
            for times in segment:
                ostring = '%d,%d\n' % (times[0],times[1])
                f.write(ostring)
    
if __name__ == "__main__":
    
    # Read in the command line prompts
    ThreeCharFile = sys.argv[1]
    DoubleCharFile = sys.argv[2]
    outputdir = sys.argv[3]
    
    # Create the output directory if it does not exist
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    
    # Read in the segment times
    ThreeCharTimes = FileReader.read_char_times(ThreeCharFile)
    DoubleCharTimes = FileReader.read_char_times(DoubleCharFile)
    SpeakerTimes = GetTalkingTimes(ThreeCharTimes,DoubleCharTimes)
    
    # Output the files
    PrintOutFiles(SpeakerTimes,outputdir)
    
