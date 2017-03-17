#!/usr/bin/python
__author__ = 'chukwuyem'

import re
import os
import sys
import nltk
import argparse
import math

max_len = 0
stopwords = nltk.corpus.stopwords.words('english')


def ngram(tweet_list, c):
    ngram_list = []
    if c=='bi': c = 1
    elif c=='tri': c = 2
    i = 0
    while i < len(tweet_list) - c:
        ngram_ = ''
        for x in range(i, i+c+1):
            ngram_ += tweet_list[x]+'|'
        ngram_ = ngram_[:-1]
        ngram_list.append(ngram_)
        i+=1
    return ngram_list


def stpwrd(tweetlist):
    newtweetlist = [w for w in tweetlist if w not in stopwords]
    return newtweetlist


def twtlen(tweet):
    tweetlist = tweet.split()
    tweet_len = "tweetLength="+str(len(tweetlist))
    return tweet_len

def twtlenbin(tweet):
    tweetlist = tweet.split()
    tlen = len(tweetlist)
    tweet_len_bin = "tweetLength="
    if tlen < 12:
        tweet_len_bin += "LOW"
    elif tlen >= 12 and tlen < 23:
        tweet_len_bin += "MID"
    else:
        tweet_len_bin += "HIGH"
    return tweet_len_bin


def targetbigram(tweet, target):
    targetbigramlist = []
    bigram_window = re.findall(r'\w*\W*\b[^A-Za-z0-9]*' + re.escape(target) + r'[^A-Za-z0-9]*\b\W*\w*', tweet,
                            flags=re.IGNORECASE)
    for bigram_window_inst in bigram_window:
        bigram_window_inst = re.sub(re.escape(target), ' THETARGET ', bigram_window_inst.lower(), flags=re.IGNORECASE)
        bigram_window_inst = re.sub(r'[^A-Za-z]', ' ', bigram_window_inst, flags=re.IGNORECASE)
        bigram_list = ngram(bigram_window_inst.split(), 'bi')
        # print bigram_list
        targetbigramlist += bigram_list
    return targetbigramlist


def targettrigram(tweet, target):
    targettrigramlist = []
    trigram_window = re.findall(r'\w*\W*\w*\W*\b[^A-Za-z0-9]*' + re.escape(target) + r'[^A-Za-z0-9]*\b\W*\w*\W*\w*',
                             tweet,
                             flags=re.IGNORECASE)
    for trigram_window_inst in trigram_window:
        trigram_window_inst = re.sub(re.escape(target), ' THETARGET ', trigram_window_inst, flags=re.IGNORECASE)
        trigram_window_inst = re.sub(r'[^A-Za-z#]', ' ', trigram_window_inst, flags=re.IGNORECASE)
        trigram_list = ngram(trigram_window_inst.split(), 'tri')
        # print trigram_list
        targettrigramlist += trigram_list
    return targettrigramlist


def rurl(tweet):
    '''at this point, the tweet already has (externalurl) in it due to external replace and lowering. this remove
    external url altogether'''
    tweet = re.sub(r'externalurl', '', tweet)
    tweet = re.sub(r'EXTERNALURL', '', tweet) #just to be safe
    return tweet


def bigrams(tweet):
    '''just bigrams in general'''
    return ngram(tweet.split(), 'bi') #returns a list of bigrams


def trigrams(tweet):
    '''just trigrams in general'''
    return ngram(tweet.split(), 'tri') #returns a list of trigrams

def senti(pos, neg):
    senti_list = []
    sentiDiff = int(pos) + int(neg)
    sentiLabel = ''
    if sentiDiff >= 0:
        sentiLabel += str(int(math.ceil(sentiDiff / 2.0)))
    else:
        sentiLabel += str(sentiDiff / 2)
    senti_list += ['sentiPos=' + pos]
    senti_list += ['sentiNeg=' + neg]
    senti_list += ['sentiNum=' + str(sentiDiff)]
    senti_list += ['sentiLabel=' + str(sentiLabel)]
    return senti_list


features = {'stpwrd': stpwrd, 'twtlen': twtlen, 'twtlenbin': twtlenbin, 'targetbi': targetbigram, 'targettri': targettrigram,
            'rurl': rurl, 'bigram': bigrams, 'trigram': trigrams, 'senti': senti}

#features in order of collection/working
# ... senti can be taken at anytime
# 1. rurl
# 2. twtlen
# 3. --- stpwrd *** actually we might need stopwords for bigrams so not yet
# 4a. targetbigram,
# 4b. targettrigram,
# 4c. bigrams,
# 4d. trigrams
# 4e. senti
# 5. stpwrd


def lineprocess(line, flag, feature_list):
    global max_len
    line_list = line.split('\t')
    tweet = line_list[5]

    urlReg = re.compile(r'https?://\S*')
    tweet = urlReg.sub(r'EXTERNALURL', tweet)
    # print tweet

    tweet = re.sub('[^0-9a-zA-Z#_@\'+/-]+', ' ', tweet.lower())
    if 'rurl' in feature_list:
        tweet = features['rurl'](tweet)
        #dictionary['key']()

    tweet_list = tweet.split()
    if 'twtlen' in feature_list: #this is done now when tweet_list is just tweet words
        tweet_list += [features['twtlen'](tweet)]
    if 'twtlenbin' in feature_list:
        tweet_list += [features['twtlenbin'](tweet)]
    if 'targetbi' in feature_list:
        tweet_list += features['targetbi'](tweet, line_list[3])
    if 'targettri' in feature_list:
        tweet_list += features['targettri'](tweet, line_list[3])
    if 'bigram' in feature_list:
        tweet_list += features['bigram'](tweet)
    if 'trigram' in feature_list:
        tweet_list += features['trigram'](tweet)
    if 'senti' in feature_list:
        tweet_list += features['senti'](line_list[0], line_list[1])
    if 'stpwrd' in feature_list:
        tweet_list = features['stpwrd'](tweet_list)

    if flag == "TRAIN":
        tweet_list += [line_list[4]]
    elif flag == "TEST":
        tweet_list += ['UNKNOWN']
    if len(tweet_list) > max_len:
        max_len = len(tweet_list)
    return tweet_list


def write_file(thefilename, thelist, folder):
    global max_len
    #remember, you're writing CRF files into new folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    h = open(os.path.join(folder, thefilename), 'w+')
    for tList in thelist:
        while len(tList) < max_len:
            tList.insert(-1, '*')
        #print len(tList), max_len
        if len(tList) != max_len:
            print 'ERROR!!'
            sys.exit()
        h.write('\t'.join(tList))
        h.write('\n')
        h.write('\n')
    h.close()


def main_function(trainFilesList, testFile, expID, feat_list):
    '''

    :param trainfiles: this is a list of training files. it comes as a list, thanks to argparser
    :param testFile: this is the one test file
    :param expID: this will be the name of the folder
    :param feat_list: this is the list of features
    :return:
    '''
    print "script 1 is up and running"
    global max_len
    train_data = []
    test_data = []

    #trainfiles = trainFilesList.split('+')

    for trainfile in trainFilesList:
        f1 = open(trainfile, 'r')

        for line in f1:
            f1_tweet_list = lineprocess(line,'TRAIN', feat_list)
            # print 'f1 ', f1_tweet_list
            train_data.append(f1_tweet_list)

        f1.close()

    f2 = open(testFile, 'r')

    for line in f2:
        f2_tweet_list = lineprocess(line, 'TEST', feat_list)
        test_data.append(f2_tweet_list)

    f2.close()

    #writing to CRF train file
    tr_name = 'crfTrain_'+expID+'.txt'
    write_file(tr_name, train_data, expID)

    #writing to CRF test file
    ts_name = 'crfTest_'+expID+'.txt'
    write_file(ts_name, test_data, expID)

    # sanity-check file = README (expID)
    if not os.path.exists(expID):
        # it should exist. if it doesn't
        print 'WARNING: folder to write sanity check file does not exist'
        os.makedirs(expID)
    sanity = 'README ('+expID+').txt'
    s = open(os.path.join(expID, sanity), 'w+')
    s.write('This is sanity check file, i.e. a README\n')
    s.write('The training file(s):\n')
    s.write(' '.join(trainFilesList)+'\n')
    s.write('The test file:\n')
    s.write(testFile)
    s.write('\nThe features used: \n')
    s.write(' '.join(feat_list))
    s.close()

    templateFunction(max_len-1, expID) #because max_len includes the sentiment label


def templateFunction(length_, folder):
    print "max_len is ", length_
    # remember, you're writing template file into same folder as CRF
    if not os.path.exists(folder):
        # it should exist. if it doesn't
        print 'WARNING: folder to write template file does not exist'
        os.makedirs(folder)
    tf_name = 'templateFile_' + folder + '.txt'
    g = open(os.path.join(folder, tf_name), 'w+')

    curr_word = 0
    count = 0
    for x in range(length_):
        # template = 'U' + str(count).zfill(6) + ':%x[' + str(curr_word) + ',' + str(count) + ']\n'
        template = 'U' + ':%x[' + str(curr_word) + ',' + str(count) + ']\n'

        count += 1
        g.write(template)

    g.close()

parser = argparse.ArgumentParser()
parser.add_argument('-i', nargs='+', dest='train_files')
parser.add_argument('-o', nargs=1, dest='test_file')
parser.add_argument('-f', nargs='*', dest='features')
parser.add_argument('-e', nargs=1, dest='experiment_id')

results = parser.parse_args()
# print 'training files = ', results.train_files
# print 'test file = ', results.test_file
# print 'features = ', results.features
# print 'experiment id = ', results.experiment_id

if results.features:
    if set(results.features).issubset(set(features.keys())):
        print "All Features Valid"
    else:
        print "ERROR: unknown feature detected"
        print "list of features: ", ' '.join(features.keys())
        sys.exit(2)

# print "it shouldn't reach here if there is an error is feature"


# main_function(['tmp.txt'], 'tmp.txt', 'exp000', ['rurl', 'twtlen', 'bigram', 'stpwrd', 'targetbi', 'senti'])
main_function(results.train_files, results.test_file[0], results.experiment_id[0], results.features)