# Jessica Ouyang
# make_file_list.py <directory>
# List all files in directory

import os
import sys

def main(args):
    if len(args) < 2:
        print 'This script takes one argument: the directory for which to list the files.'
        return 1

    for (dirpath, _, filenames) in os.walk(args[1]):
        for filename in filenames:
            print  dirpath + filename        

if __name__ == '__main__':
    sys.exit(main(sys.argv))
