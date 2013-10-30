#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by Joe Ellis and Jessica Ouyang
# Logistic Progression
# Natural Language Processing, Machine Learning, and the Web

import sys


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

if __name__ == "__main__":
    # Descriiption: This function takes the gold real standard labels and the predicted labels file, and
    # evaluates the day-level accuracy, month-level accuracy, and year-level accuracy and outputs these accuracies to
    # the standard output
    # Inputs:
    #   - gold_file = The file that contains the gold results
    #   - prediction_file = The file that contains the predicted results

    # Read in the inputs
    gold_file = sys.argv[1]
    pred_file = sys.argv[2]

    with open(gold_file, "r") as g:
        lines_raw = g.readlines()
        gold_dates = [line.rstrip("\n") for line in lines_raw]
    with open(pred_file, "r") as f:
        lines_raw = f.readlines()
        pred_dates = [line.rstrip("\n") for line in lines_raw]

    total_dates = float(len(pred_dates))
    correct_day_count = 0
    correct_month_count = 0
    correct_year_count = 0
    for pred_date,gold_date in zip(pred_dates,gold_dates):
        pred_day,pred_month,pred_year = SeperateDate(pred_date)
        gold_day,gold_month,gold_year = SeperateDate(gold_date)

        # Now let's check for our three levels of correctness
        if (pred_day == gold_day) and (pred_month == gold_month) and (pred_year == gold_year):
            correct_day_count += 1
            correct_month_count += 1
            correct_year_count += 1
        elif (pred_month == gold_month) and (pred_year == gold_year):
            correct_month_count += 1
            correct_year_count += 1
        elif (pred_year == gold_year):
            correct_year_count += 1

    # Now let's output the results to the screen
    print "Day-Level Accuracy = ", correct_day_count / total_dates
    print "Month-Level Accuracy = ", correct_month_count / total_dates
    print "Year-Level Accuracy = ", correct_year_count / total_dates