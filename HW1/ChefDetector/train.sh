#!/bin/bash                                                                     
if [ $# -ne 5 ]
then
    echo "Unexpected number of arguments: please give (1) which feature set to use (\"bagofwords\", \"backoff\", \"trigram\"), (2) the training label file, (3) the test label file, (4) the directory of recipe files, and (5) the file for saving the trained model."
    exit 2
fi

ant clean
ant compile
ant doc

mkdir -p ./temp/

java -Xmx2G -cp ./bin:./lib/mallet.jar:./lib/mallet-deps.jar src.AlphabetBuilder $1 $2 $3 $4 temp/

java -Xmx2G -cp ./bin:./lib/mallet.jar:./lib/mallet-deps.jar src.InstanceBuilder $1 temp/

java -Xmx2G -cp ./bin:./lib/mallet.jar:./lib/mallet-deps.jar src.Trainer $1 temp/ $5