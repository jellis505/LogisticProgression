#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Created by Joe Ellis and Jessica Ouyang
# Logistic Progression 
# Natural Language Processing, Machine Learning, and the Web

import os
import sys

# Append the path to the FreeBase Module I created
sys.path.append("FreeBase")
from pyFreeBase import FreeBase

def SeperateDate(date_string):
    # Description: returns the month, day, and year of the strings
    # Inputs:
    #   - date_string = The string variable containing the date held in "DD-MM-YYYY"
    # Outputs:
    #   - Month = Integer Value of Month
    #   - Day = Integer Value of Month
    #   - Year = Integer Value of Month
    parts = date_string.split("-")
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return day,month,year


def ReturnNameandBirth(name_file,birthday_file):
    # Description:  This function reads in the birthdays and names from the files,
    # and then returns a tuple of the values
    # Inputs:
    #   -name_file = The path to the name_file (new line seperated)
    #   -birthday_file = The path to the file containing the birthdays (new line sepereated)
    # Outputs:
    #   - names = list of the names from the file
    #   - bday = list of the birthdays for each name

    n = open(name_file,"r")
    b = open(birthday_file, "r")
    raw_name_lines = n.readlines()
    raw_bday_lines = b.readlines()
    names = [line.rstrip("\n") for line in raw_name_lines]
    bday = [line.rstrip("\n") for line in raw_bday_lines]
    
    return names,bday

def GetDayError(ground_truth,found_data):
    # Description: Calculates the amount of days our found date is off from the ground truth
    # Inputs:
    #   - ground_truth = The ground truth data in (month,day,year)
    #   - found_data = The FreeBase result (month,day,year)
    # Outputs:
    #   - error = The number of days we are off by our guess
    
    # estimating that each month has 30 days
    err_mon = 30*(ground_truth[0]-found_data[0])
    err_day = (ground_truth[0]-found_data[0])
    err_y = 365*(ground_truth[0]-found_data[0])
    return err_mon + err_day + err_y
    

if __name__ == "__main__":
    # Description: This function runs the test for finding birthdays from structured data,
    # using the FreeBase module and API that we designed.
    # Inputs:
    #   - name_file = The new lined seperated file that contains the names
    #   - birthday_file = The new lined seperated file that contains the birthdays
    
    # Read in the inputs
    name_file = sys.argv[1]
    birthday_file = sys.argv[2]
    
    # Read in the files for analysis
    names,bday = ReturnNameandBirth(name_file,birthday_file)
    
    # Now loop through and get the error for each of these
    final_results = []
    # Initalize the class variable
    free_base = FreeBase()
    
    # This list will hold the error in days
    error_days = []
    correct = 0
    missed = 0
    for name, bday in zip(names,bday):
        g_day,g_month,g_year = SeperateDate(bday)
        result = free_base.GetQuery(name)
        month, day, year = free_base.GetBirthday(result)
        error = GetDayError((g_month, g_day,g_year),(month,day,year))
        error_days.append(error)
        
        # Count up to see the number of correct and the number of errors
        if error == 0:
            correct += 1
        else:
            missed += 1
    
    # Output the results to the screen
    print "We correctly found %d birthdays out of %d for %f accuracy" % (correct, correct + missed, correct / float(correct + missed))
    print "The total number of days in error was: %d" % sum(error_days)
