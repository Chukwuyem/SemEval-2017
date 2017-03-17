#!/usr/bin/python
__author__ = 'chukwuyem'

def main_function(filename, h):
    f = open(filename, 'r')

    for line in f:
        line_list = line.split('\t')
        label5p = int(line_list[3])
        label3p = ''
        if label5p > 0: label3p += 'positive'
        elif label5p == 0: label3p += 'neutral'
        elif label5p < 0: label3p += 'negative'
        new_line_list = [line_list[0], line_list[1], line_list[2], label3p, line_list[4]]
        #print '\t'.join(new_line_list)
        new_line = '\t'.join(new_line_list)
        h.write(new_line)
        h.write('\n')

    f.close()

listFiles = ["taskC_data.txt", "senti_data_twitter_noTopic_senti.txt"]

h_name = 'extra_train_taskC_senti.txt'
h = open(h_name, 'w+')
for x in listFiles:
    main_function(x, h)
# main_function('tmpTrainA.txt', h)
h.close()