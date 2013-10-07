!/bin/bash                                                                                                                                                                                                 
if [ $# -ne 3 ]
then
    echo "Unexpected number of arguments: please give (1) which feature set to use (\"bagofwords\", \"backoff\", \"trigram\"), (2) the saved trained model, and (3) the output filename."
    exit 2
fi

java -Xmx2G -cp ./bin:./lib/mallet.jar:./lib/mallet-deps.jar src.Tester $1 temp/ $2 $3