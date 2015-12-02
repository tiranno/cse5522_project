#!/usr/bin/python
import csv
import re
import nltk
import sys
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

def f_import_raw_input(filenames):

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    passages = []
    for  filename in filenames:
        raw_text = ''
        with open(filename, 'r') as f:
            raw_text = f.read()
            f.close()

        raw_text = raw_text.replace('?"', '? "').replace('!"', '! "').replace('."', '. "').replace("\n", ' ')
        passages.append(sent_detector.tokenize(raw_text, realign_boundaries=True))

    return passages

def f_parse_raw_input(filename):
    passages = f_import_raw_input(filename)


    ngrams = []
    for sentences in passages:
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            if tokens[-1] == ".":
                del tokens[-1]

            # print(tokens)
            win_index = 2
            while len(tokens) > 2 and win_index < len(tokens):
                one = tokens[win_index-2].rstrip("\'").lstrip("\'")
                two = tokens[win_index-1].rstrip("\'").lstrip("\'")
                three = tokens[win_index].rstrip("\'").lstrip("\'")
                if one in "?.,();:" or one == "--" or one == "``" or one == "\'\'" or one =="\'":
                    win_index = win_index + 1
                elif two in "?.,();:\'" or two == "--" or two == "``" or two == "\'\'" or two =="\'":
                    win_index = win_index + 1
                elif three in "?.,();:\'" or three == "--" or three == "``" or three == "\'\'" or three =="\'":
                    win_index = win_index + 1
                else:
                    gram = [one, two, three]
                    ngrams.append(gram)
                    win_index = win_index + 1


    counting_dict = {}
    for gram in ngrams:
        gram_string = gram[0]+','+gram[1]+','+gram[2]
        if gram_string in counting_dict:
            counting_dict[gram_string] = counting_dict[gram_string] + 1
        else:
            counting_dict[gram_string] = 1

    gram_count = []
    for gram, value in counting_dict.items():
        gram_count.append([value]+gram.split(','))

    # print(gram_count)
    probability_grams = f_calc_two_window(gram_count)
    print(probability_grams)
    # print(counting_dict)


def f_write_to_csv(grams):
    with open('generated_cpt.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for gram in grams:
            writer.writerow(gram)
        csvfile.close()

def f_parse_common_three_grams():
    total_words = 0
    three_grams = [] #[count, first word, second word, third word]
    with open('w3_.txt', encoding="ISO-8859-1") as f:
        number = 0
        for line in f:
            gram = line.split('\t')
            three_grams.append(gram)

    probability_grams = f_calc_two_window(three_grams)
    f_write_to_csv(probability_grams)

#Put this in the editor if we want to have live updating from the user input
def f_calc_two_window(grams):
    new_grams = [] #[frequency given window, first word, second word, third word]

    current_window = []
    current_window_total = 0
    counting_dict = {}
    for row in grams:
        if current_window != [row[1], row[2]]:
            #Calculate probability of counted for n=2 window
            for key, value in counting_dict.items():
                prob_given_window = value/float(current_window_total)
                new_grams.append([prob_given_window] + current_window + [key])

            #Reset variables
            current_window = [row[1], row[2]]
            current_window_total = 0
            counting_dict = {}

        if current_window == [row[1], row[2]]:
            counting_dict[row[3].rstrip('\n')] = int(row[0])
            current_window_total = current_window_total + int(row[0])

    return new_grams


if __name__ == '__main__':
    # f_parse_common_three_grams()

    reload(sys)
    sys.setdefaultencoding('utf8')

    raw_text_files = ['sherlock_1.txt','sherlock_2.txt',#'sherlock_3.txt',
        'sherlock_4.txt','sherlock_5.txt','sherlock_6.txt','sherlock_7.txt',
        'sherlock_8.txt','sherlock_9.txt','sherlock_10.txt','sherlock_11.txt',
        'sherlock_12.txt']
    f_parse_raw_input(raw_text_files)
