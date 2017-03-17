#!/usr/bin/python
__author__ = 'chukwuyem'

import os
import sys


def main_function(testFile, crfFile, expfolder):
    if not os.path.exists(expfolder):
        #this is an error
        print "ERROR: Folder "+expfolder+" does not exist"
        sys.exit(1)

    f1 = open(testFile, 'r') #remember this is in the current folder
    f2 = open(crfFile, 'r')

    f3_name = ''.join([testFile.replace(".txt", ""), "_GUESS.txt"])
    f3 = open(os.path.join(expfolder, f3_name), 'w+')

    #remember for SE 2017, the test file gold and the test file guess are in the format
    # <tweet id> <target> <label>

    for line in f1:
        tweet_data = line.split('\t')[2:4] #remember, this script is for those files with senti data at the beginning
        f2_guessed_str = f2.readline()
        f2_guess = f2_guessed_str.split('\t')[-1]  # this is the guessed label

        # print f2_guessed_str.split('\t')
        # print f2_guess, type(f2_guess)
        # f2_guess[0] = f2_guess[0][:-1]  # remove the return carriage character '\r' at the end of the label

        return_str = tweet_data + [f2_guess]
        return_str = '\t'.join(return_str)
        f3.write(return_str)
        #print return_str

        f2_guessed_str = f2.readline() #to skip the empty line

    f1.close()
    f2.close()
    f3.close()

# main_function("test data", "crfTest_GUESS")
main_function(sys.argv[1], sys.argv[2], sys.argv[3])