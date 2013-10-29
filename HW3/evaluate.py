# Jessica Ouyang
# evaluate.py <gold years> <predicted years>
# Evaluate a predicted birth year using accuracy and root mean squared error

import math
import sys

def main(args):
    if len(args) < 3:
        print "This script takes two arguments: the filename for the gold birth years and the filename for the predicted birth years."
        return 1
    
    goldf = open(args[1])
    predictedf = open(args[2])
    
    gold_years = [int(x.strip().split(r'-')[2]) for x in goldf.readlines()[:-1]]
    predicted_years = [int(x.strip()) for x in predictedf.readlines()]

    goldf.close()
    predictedf.close()

    total_years = len(gold_years)
    if total_years != len(predicted_years):
        print "Number of gold birth years different from number of predicted birth years: " + str(total_years) + " vs " + str(len(predicted_years))
        return 1

    accuracy = 0
    rmse = 0

    for i in range(total_years):
        accuracy += (gold_years[i] == predicted_years[i])
        rmse += pow(gold_years[i] - predicted_years[i], 2)
    total_years = float(total_years)
    accuracy /= total_years
    rmse = math.sqrt(rmse / total_years)

    print "Accuracy: " + str(accuracy)
    print "RMSE: " + str(rmse)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

