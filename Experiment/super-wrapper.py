#!/usr/bin/python
__author__ = 'chukwuyem'

import subprocess, shlex

features = ['stpwrd', 'twtlen', 'twtlenbin', 'rurl', 'bigram', 'senti']


# feature_combo = [[1,2,3,4,5,6], [1,2,3,4,6], [1,3,4,5,6], [1,2,4,5,6], [1,2,3,5,6], [1,2,3,6], [1,2,4,6], [1,2,5,6],
#                  [1,3,4,6], [1,3,5,6], [1,4,5,6], [2,3,4,6], [2,3,5,6], [1,2,6], [1,3,6], [1,4,6], [1,5,6], [2,3,6],
#                  [2,4,6], [2,5,6], [3,4,6], [3,5,6], [4,5,6], [1,6], [2,6], [3,6], [4,6], [5,6], [2,4,5,6], [3,4,5,6], [6]]

feature_combo = [[1,2,3,4,5,6], [1,2,3,4,5], [1,3,4,5,6], [1,2,4,5,6], [1,2,3,5,6], [1,2,3,4,6], [1,2,3,4], [1,2,3,5],
                 [1,2,3,6], [1,3,4,5], [1,3,4,6], [1,4,5,6], [2,3,4,5], [2,3,4,6], [2,4,5,6], [3,4,5,6], [1,2,4,5],
                 [1,2,4,6], [1,2,5,6], [1,2,3], [1,2,4], [1,2,5], [1,2,6], [1,3,4], [1,3,5], [1,3,6], [1,4,5], [1,4,6],
                 [1,5,6], [2,3,4], [2,3,5], [2,3,6], [2,4,5], [2,4,6], [3,4,5], [3,4,6], [3,5,6], [4,5,6], [1,2], [1,3],
                 [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6], [1], [2], [3],
                 [4], [5], [6]]


train_files = ['nontaskB_training_senti_PURE_dub-neutral.txt', 'nontaskB_training_senti_PURE_no-neutral.txt',
            'taskB_training_senti-no-off_PURE_dub-neutral.txt', 'taskB_training_senti-no-off_PURE_no-neutral.txt']

test_file = "test2016-2point_senti.txt"
test_file_gold = "test2016-2point-test.txt"
gold_aggreg = "test2016-2point-test.txt.aggregate"

train_combo = [[1,3], [2,4]]



def run_function():
    #create file that will take perl eval outputs
    e = open("listOfScores.txt", "w+")
    e2 = open("listOfScoresAggreg.txt", "w+")
    experID = 0

    for tr_combo in train_combo:
        for feat_combo in feature_combo:
            expIDstr = 'expr-'+str(experID)
            script1command = ['python', 'script-1-crf.py ']
            script1command += ['-i']
            script1command += [train_files[w-1] for w in tr_combo]
            script1command += ['-o', test_file]
            script1command += ['-f']
            script1command += [features[w-1] for w in feat_combo]
            script1command += ['-e']
            script1command += [expIDstr]
            print 'running... ', ' '.join(script1command)
            subprocess.call(' '.join(script1command), shell=True)

            templFile = expIDstr+"/templateFile_" + expIDstr + '.txt'
            crflearnFile = expIDstr+"/crfTrain_" + expIDstr + '.txt'
            modelFile = expIDstr+"/modelFile_" + expIDstr
            crflearncommand = ["crf_learn", templFile, crflearnFile, modelFile]
            print 'running... ', ' '.join(crflearncommand)
            subprocess.call(' '.join(crflearncommand), shell=True)

            crftestFile = expIDstr+"/crfTest_" + expIDstr + '.txt'
            crftestGUESSFile = expIDstr+"/crfTest_" + expIDstr + '_GUESS.txt'
            crftestcommand = ["crf_test", "-m", modelFile, crftestFile, ">", crftestGUESSFile]
            print 'running... ', ' '.join(crftestcommand)
            subprocess.call(' '.join(crftestcommand), shell=True)

            script3command = ["python", "script-3-crf.py", test_file, crftestGUESSFile, expIDstr]
            print 'running... ', ' '.join(script3command)
            subprocess.call(' '.join(script3command), shell=True)

            test_file_guess = expIDstr+"/test2016-2point_senti_GUESS.txt"
            evalcommand = ["perl", "score-semeval2016-task4-subtaskB.pl", test_file_gold, test_file_guess]
            print 'running... ', ' '.join(evalcommand)
            evaloutput = subprocess.check_output(' '.join(evalcommand), shell=True)
            thisFeats = ' '.join([features[w-1] for w in feat_combo] + [train_files[w-1] for w in tr_combo])
            e.write(thisFeats+'\t'+evaloutput)
            e.write('\n')

            aggregcommand = ['perl', 'aggregate-semeval2016-task4-subtaskD.pl', test_file_guess]
            print 'running...', ' '.join(aggregcommand)
            subprocess.call(' '.join(aggregcommand), shell=True)

            guess_aggreg = test_file_guess + '.aggregate'
            aggregevalcommand = ['perl', 'score-semeval2016-task4-subtaskD.pl', gold_aggreg, guess_aggreg]
            print 'running...', ' '.join(aggregevalcommand)
            aggregevaloutput = subprocess.check_output(' '.join(aggregevalcommand), shell=True)
            e2.write(expIDstr+'\t'+aggregevaloutput)
            e2.write('\n')
            print '\n'

            experID += 1

    e.close()
    e2.close()


run_function()