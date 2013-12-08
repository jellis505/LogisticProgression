# extract_features.py
# Jessica Ouyang
# 02 Dec 2013


import os
import os.path
import re
import sys


# Ngrams

# return - list of lists, where each ngram is a list of length n
def get_ngrams(slist, negation_bitmap, n):
    ngrams = []
    for i in range(len(slist)-n+1):
        ngram = []
        for j in range(n):
            s = slist[i+j]
            if negation_bitmap[i+j]:
                s = s + '_NEG'
            ngram.append(s)
        ngrams.append(ngram)
    return ngrams


# Lexicon

# return - (num tokens with score > 0, total score, max score, score of last token with score > 0)
def lexicon_lookup(slist, lexicon_filename):
    f = open(lexicon_filename, 'r')
    lexicon = [line.strip() for line in f]
    f.close()

    is_nrc = 'NRC' in lexicon_filename

    count, total, max, last = 0.0, 0.0, 0.0, 0.0
    for entry in lexicon:
        word, score, _, _ = entry.split()
        if word[0] == '@': # skip at-mentions
            continue
        if word[0] == '#': # remove hashtags
            word = word[1:]

        score = float(score)
        if is_nrc: 
            score /= 8 # normalize score
        else:
            score /= 5
        for i in range(len(slist)):
            s = slist[i]
            if s == word:
                if score > 0:
                    count += 1
                    last = score
                total += score
                if score > max:
                    max = score
    return (count, total, max, last)
        

# Negation

negation = ['never', 'no', 'nothing', 'nowhere', 'none', 'not', 'haven\'t', 'hasn\'t', 'hadn\'t', 'can\'t', 'shouldn\'t', 'won\'t', 'wouldn\'t', 'don\'t', 'doesn\'t', 'isn\'t', 'aren\'t', 'ain\'t']

# return - list of tuples (negation word index, punctuation index)
def extract_negations(slist):
    negations = []
    for i in range(len(negation)):
        if negation[i] in slist:
            not_index = slist.index(negation[i])
            end_index = len(slist)
            context = slist[not_index+1:]
            if '.' in context:
                end_index = context.index('.') + not_index
            negations.append((not_index, end_index))
    return negations

# return - a list bitmap (true if word is in negated context, false else)
def get_negation_bitmap(slist, negations):
    bitmap = [False] * len(slist)
    if len(negations) == 0:
        return bitmap
    i = 0
    start, end = negations[i]
    for j in range(len(slist)):
        if j >= start:
            if j < end:
                bitmap[j] = True
            elif j == end:
                bitmap[j] = True
                i += 1
                if i >= len(negations):
                    break
                start, end = negations[i]
    return bitmap


# Main

def main(file_dirname, feature_dirname, lexicons):
    files = [f for f in os.listdir(file_dirname) if os.path.isfile(os.path.join(file_dirname,f))]
    for file in files:
        f = open(os.path.join(file_dirname, file), 'r')
        lines = [line.strip() for line in f]
        f.close()

        slist = ' . '.join(lines).split()
        negations = extract_negations(slist)
        negation_bitmap = get_negation_bitmap(slist, negations)
        
        outf = open(os.path.join(feature_dirname, file), 'w')

        for i in range(5):
            ngrams = get_ngrams(slist, negation_bitmap, i)
            for ngram in ngrams:
                if len(ngram) > 0:
                    print >>outf, '_'.join(ngram) + ',' + str(1)

        for i in range(len(lexicons)):
            lex_features = lexicon_lookup(slist, lexicons[i])
            print >>outf, 'lex' + str(i) + '_count,' + str(lex_features[0])
            print >>outf, 'lex' + str(i) + '_total,' + str(lex_features[1])
            print >>outf, 'lex' + str(i) + '_max,' + str(lex_features[2])
            print >>outf, 'lex' + str(i) + '_last,' + str(lex_features[3])

        print >>outf, 'num_negations,' + str(len(negations))
        
        outf.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
