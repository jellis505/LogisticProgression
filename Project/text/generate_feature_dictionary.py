# generate_feature_dictionary.py
# Jessica Ouyang


import os
import os.path
import sys


def main(feature_dirname, dict_filename):
    features = set()
    files = [f for f in os.listdir(feature_dirname) if os.path.isfile(os.path.join(feature_dirname,f))]
    for file in files:
        f = open(os.path.join(feature_dirname, file), 'r')
        for line in f:
            features.add(line.split(',')[0])
        f.close()
        
    outf = open(dict_filename, 'w')
    for feature in features:
        print >>outf, feature
    outf.close()

if __name__ == '__main__':
    sys.exit(main(*(sys.argv[1:])))
