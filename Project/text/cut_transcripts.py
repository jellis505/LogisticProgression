# preprocess.py
# Jessica Ouyang


import os
import os.path
import re
import sys


label_pat = re.compile(r"^[0-9]+$")
time_pat = re.compile(r"(?P<start>[0-9]{2}\:[0-9]{2}\:[0-9]{2}\,[0-9]{3}) --\> (?P<end>[0-9]{2}\:[0-9]{2}\:[0-9]{2}\,[0-9]{3})")


# return - number of seconds (rounded)
def standardize_time(str):
    if '.' in str: # from cut video's time file
        seconds, remainder = map(int, str.split('.'))
        if remainder > 49:
            seconds += 1
        return seconds

    time, remainder = str.split(',') # from transcript file
    remainder = int(remainder)
    hours, minutes, seconds = map(int, time.split(':'))
    minutes += 60 * hours
    seconds += 60 * minutes
    if remainder > 499:
        seconds += 1
    return seconds


# return - percent of span2 that is contained in span1
def percent_overlap(span1, span2):
    start1, end1 = span1
    start2, end2 = span2
    if start2 < start1:
        if end2 < start1:
            return 0 
        return float(end2-start1) / end2 - start2
    if end2 < end1:
        return 1
    return float(end1-start2) / end2 - start2


def main(transcript_filename, time_filename, output_dirname):
    f = open(transcript_filename, 'r')
    transcript = f.readlines()
    f.close()
    f = open(time_filename, 'r')
    times = f.readlines()
    f.close()

    i = 0
    video_name = time_filename[time_filename.rfind('/')+1:time_filename.find('.')]
    for segment in times:
        label, start1, end1 = segment.strip().split(',')
        start1, end1 = standardize_time(start1), standardize_time(end1)
        
        outf = open(os.path.join(output_dirname, video_name + '_' + label), 'w')

        while i < len(transcript):
            line = transcript[i].strip()
            i += 1

            if re.match(label_pat, line): 
                continue
            
            match = re.match(time_pat, line)
            if  match:
                start2, end2 = standardize_time(match.group('start')), standardize_time(match.group('end'))
                if percent_overlap((start1, end1), (start2, end2)) < 0.25: # if at least 75% of transcript span doesn't overlap the current segment, move on to next segment
                    break
                  
            else:
                print >>outf, line
                        
        outf.close()

         
if __name__ == '__main__':
    sys.exit(main(*(sys.argv[1:])))
