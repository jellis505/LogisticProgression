# train.py
# Jessica Ouyang

import os
import os.path
import sys

from sklearn import svm

# return - dictionary from all filenames to gold labels
def read_instances(gold_dirname):
    labels = {}
    golds = [f for f in os.listdir(gold_dirname) if os.path.isfile(os.path.join(gold_dirname,f))]
    for gold in golds:
        f = open(os.path.join(gold_dirname, gold), 'r')
        entries = [line.strip() for line in f]
        f.close()
        for entry in entries:
            if len(entry.split(',')) == 5:
                continue
            filename, _, label, clean = entry.split(',')
            labels[filename] = int(label)
    return labels    


# return - (train filenames, test filenames)
def partition(labels, train_proportion):
    filenames = labels.keys()
    num_train = int(float(train_proportion) * len(filenames) + 0.5)
    return (filenames[:num_train], filenames[num_train:])


def build_feature_vector(filename, feature_dictionary):
    f = open(filename, 'r')
    file = [line.strip() for line in f]
    f.close()
    vector = [0] * len(feature_dictionary)
    for i in range(len(feature_dictionary)):
        feature = feature_dictionary[i]
        for line in file:
            name, value = line.split(',')
            if name == feature:
                vector[i] = value
    return vector


def main(gold_dirname, feature_dirname, feature_dictionary_filename, train_proportion):
    all = read_instances(gold_dirname)
    train, test = partition(all, train_proportion)
    
    f = open(feature_dictionary_filename, 'r')
    feature_dictionary = [line.strip() for line in f]
    f.close()

    trainx, trainy = [], []
    for instance in train:
        trainx.append(build_feature_vector(os.path.join(feature_dirname, instance), feature_dictionary))
        trainy.append(all[instance])

    model = svm.SVC()
    model.fit(trainx, trainy)
    
    testx, testy = [], []
    for instance in test:
        testx.append(build_feature_vector(os.path.join(feature_dirname, instance), feature_dictionary))
        testy.append(all[instance])
    
    predictions = model.predict(testx)
    num_correct = 0
    for i in range(len(test)):
        if predictions[i] == testy[i]:
            num_correct += 1
    print 'Accuracy: ' + str(float(num_correct) / len(test))

if __name__ == '__main__':
    sys.exit(main(*(sys.argv[1:])))
