#!/usr/bin/python
__author__ = 'chukwuyem'


def function(filename):
    f = open(filename, 'r')

    h1_name = ''.join([filename.replace(".txt", ""), "_dub-neutral.txt"])
    h1 = open(h1_name, 'w+')
    h2_name = ''.join([filename.replace(".txt", ""), "_no-neutral.txt"])
    h2 = open(h2_name, 'w+')
    neut = 0
    nonNeut = 0


    for line in f:
        line_list = line.rstrip().split('\t')
        label = line_list[4]
        #print label

        if label == 'neutral': #neutral
            neut += 1
            #for neutral tweets, create pos and neg versions and write to h1
            #DO NOT WRITE TO h2
            newlist = [line_list[0], line_list[1], line_list[2], line_list[3], 'positive', line_list[5]]
            newline = '\t'.join(newlist)
            h1.write(newline)
            h1.write('\n')
            newlist = [line_list[0], line_list[1], line_list[2], line_list[3], 'negative', line_list[5]]
            newline = '\t'.join(newlist)
            h1.write(newline)
            h1.write('\n')
        else: #non-neutral
            nonNeut += 1
            #for non-neutral tweets, write to h1 and h2
            newlist = [line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5]]
            newline = '\t'.join(newlist)
            h1.write(newline)
            h1.write('\n')
            h2.write(newline)
            h2.write('\n')




    h1.close()
    h2.close()

    f.close()

    print 'neutrals= ', neut, '; non-neutrals= ', nonNeut

function('taskB_training_senti-no-off_PURE.txt')