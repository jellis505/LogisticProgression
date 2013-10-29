# Jessica Ouyang
# get_dates.py <webpage directory>
# Create a Professor from a webpage

import os
import re
import sys

class Professor:
    # A class for storing dates associated with a professor.
    # undergrad - year of undergrad degree
    # masters - year of masters degree
    # phd - year of phd degree

    def __init__(self):
        self.undergrad = None
        self.masters = None
        self.phd = None


undergrad_keywords = ['B.A.', 'B.S.', 'B.A.S', 'B.Phil', 'Ph.B', 'B. Phil']
masters_keywords = ['M.B.A', 'M.A', 'M.S', 'M.Phil', 'Ph.M', 'M. Phil']
phd_keywords = ['Ph.D.']

date_regex = re.compile(r'[1-2][\d]{3}')


def make_professor(lines):
    # This is a simple and naive way to search for degree dates.
    # lines - the scraped webpage for the professor
    # returns - a Professor with the dates found
    prof = Professor()
    for i in range(len(lines)):
        line = lines[i]
        match = re.search(date_regex, line)
        if match:
            found = False
            date = int(match.group(0))
            for keyword in undergrad_keywords:
               if keyword in line or keyword in lines[i-1] or (i < len(lines) - 1 and keyword in lines[i+1]):
                   prof.undergrad = date
                   found = True
                   break
               if not found:
                   for keyword in masters_keywords:
                       if keyword in line or keyword in lines[i-1] or (i < len(lines) - 1 and keyword in lines[i+1]):
                           prof.masters = date
                           found = True
                           break
               if not found:
                   for keyword in phd_keywords:
                       if keyword in line or keyword in lines[i-1] or (i < len(lines) - 1 and keyword in lines[i+1]):
                           prof.phd = date
                           found =True
                           break
    return prof


def main(args):
    # Predict birth years for all webpages in a directory
    # args - args[1] expected to be the list of people
    #      - args[2] expected to be the name of the directory
    #      - args[3] if present is the year to use if no year can be predicted
    # writes predicted years to 'predictions.txt'
    
    if len(args) < 3:
        print 'This script takes two arguments: the list of people and the directory of webpages.'
        return 1

    # sum and number of birthdates found
    found_dates = []
    date_sum = 0
    num_dates = 0

    f = open(args[1], 'r')
    names = f.readlines()
    f.close()
    
    for name in names: 
        name = name.strip()
        f = open(args[2] + name + '.txt')
        lines = f.readlines()
        f.close()
        prof = make_professor(lines)

        date = None
        if prof.undergrad:
            date = prof.undergrad - 22 # assume people finish undergrad at 22
        elif prof.masters:
            date = prof.masters - 24 # assume 2-year masters
        elif prof.phd:
            date = prof.phd - 27 # assume 5-year phd

        if date:
            found_dates.append(date)
            date_sum += date
            num_dates += 1
        else:
            found_dates.append(None)

    f = open('predictions.txt', 'w')
    average_date = int(float(date_sum) / num_dates + 0.5) # if no birthdate found for a professor, guess the average over the ones that were found
    if len(args) == 4:
        average_date = args[3] # if default year was given, use it
    for date in found_dates:
        if date:
            print >>f, date
        else:
            print >>f, average_date
    f.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
