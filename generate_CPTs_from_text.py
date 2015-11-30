#!/usr/bin/python3
import csv

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


f_parse_common_three_grams()



# for post in root.iter('Post'):
#     window = ['0', '0']
#     if post.attrib['class'] != 'System':
#         for t in post.iter('t'):
#             word = t.attrib['word']
#             if t.attrib['pos'] == '.':
#                 word = '.'
#             if t.attrib['pos'] == 'NNP':
#                 word = 'NNP'
#             strWindow = ':'.join(window)
#             instance = {'window': strWindow, 'word': word, 'count': 1}
#             seenInstance = False
#             seenWindow = False
#             for x in wordCounts:
#                 if x['window']==strWindow:
#                     if x['word'] == word:
#                         x['count'] = x['count'] + 1
#                         seenInstance = True
#                     seenWindow = True
#                     for windowInstance in windowCounts:
#                         if windowInstance['window'] == strWindow:
#                             windowInstance['count'] = windowInstance['count'] + 1
#             if not seenInstance:
#                 wordCounts.append(instance)
#             if not seenWindow:
#                 windowCounts.append({'window':strWindow, 'count': 1})
#             window[0] = window[1]
#             window[1] = word
#
# for windowCount in windowCounts:
#     for wordCount in wordCounts:
#         if windowCount['window'] == wordCount['window']:
#             wordCount['count'] = float(wordCount['count'])/float(windowCount['count'])
