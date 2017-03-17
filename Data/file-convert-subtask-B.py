#!/usr/bin/python
__author__ = 'chukwuyem'


def main_function(filename, h):
    f = open(filename, 'r')

    for line in f:
        line_list = line.rstrip().split('\t')
        label = line_list[4]
        fivePoint = []
        if label == "positive":
            fivePoint += ['1', '2']
        elif label == "negative":
            fivePoint += ['-1', '-2']
        elif label == "neutral":
            fivePoint += ['0', '0']
        else:
            continue
        new_line_list = [line_list[0], line_list[1], line_list[2], line_list[3], fivePoint[0], line_list[5]]
        new_line = '\t'.join(new_line_list)
        h.write(new_line)
        h.write('\n')
        # print new_line
        new_line_list = [line_list[0], line_list[1], line_list[2], line_list[3], fivePoint[1], line_list[5]]
        new_line = '\t'.join(new_line_list)
        h.write(new_line)
        h.write('\n')
        # print new_line

    f.close()


h_name = 'taskB_training_senti_PURE_5point.txt'
h = open(h_name, 'w+')
main_function("taskB_training_senti-no-off_PURE.txt", h)
h.close()