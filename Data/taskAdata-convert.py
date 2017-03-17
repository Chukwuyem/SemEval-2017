#!/usr/bin/python
__author__ = 'chukwuyem'

def main_function(filename, h):
    f = open(filename, 'r')

    for line in f:
        line_list = line.rstrip().split('\t')
        new_line_list = [line_list[0], '*****', line_list[1], line_list[2]]
        label = line_list[1]
        fivePoint = []
        if label == "positive":
            fivePoint += ['1', '2']
        elif label == "negative":
            fivePoint += ['-1', '-2']
        elif label == "neutral":
            fivePoint += ['0', '0']
        new_line_list = [line_list[0], '*****', fivePoint[0], line_list[2]]
        new_line = '\t'.join(new_line_list)
        h.write(new_line)
        h.write('\n')
        # print new_line
        new_line_list = [line_list[0], '*****', fivePoint[1], line_list[2]]
        new_line = '\t'.join(new_line_list)
        h.write(new_line)
        h.write('\n')
        # print new_line

    f.close()

listFiles = ["train2016-noTopic.txt", "test2016-noTopic.txt"]

h_name = 'taskA_data.txt'
h = open(h_name, 'w+')
for x in listFiles:
    main_function(x, h)
# main_function('tmpTrainA.txt', h)
h.close()