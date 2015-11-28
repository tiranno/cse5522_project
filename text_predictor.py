#!/usr/bin/python3
from time import sleep
import os
import curses, curses.panel
import sys
import csv
from operator import itemgetter

MAX_PREDICTIONS = 3

def f_import_predictions():
    prediction_list = []
    with open('CPTs.csv', 'r') as f:
        reader = csv.reader(f)
        prediction_list = list(reader)
    return prediction_list

def f_predictions(word_one, word_two, prediction_list):
    words = []
    for line in prediction_list:
        if line[0] == word_one+':'+word_two:
            word = line[-2]
            probability = line[-1]
            words.append([word, probability])

    final = []
    if len(words) > 0:
        sorted(words, key=itemgetter(1))
        for word in words:
            if len(final) != MAX_PREDICTIONS:
                final.append(word)
    return final

# Make a new panel, return it and it's related window
def f_make_panel(height, width, y, x):
   win = curses.newwin(height, width, y, x)
   win.erase()
   win.box()

   panel = curses.panel.new_panel(win)
   return win, panel

# Initializes the app in-terminal and returns the window object
def f_app_setup(app_window):
    # curses.noecho()
    # curses.cbreak()
    curses.curs_set(0)
    app_window.box()
    # app_window.keypad(1)
    app_window.addstr(0,2," TEXT PREDICTOR  |  Help: [!!!] ")

# Destroys the app in-terminal and exits the program
def f_app_teardown():
    # app_window.keypad(0)
    # curses.nocbreak()
    # curses.echo()
    curses.endwin()
    sys.exit()

# The main editor function. Loops until given signal to quit
def f_editor(app_window):
    prediction_list = f_import_predictions()

    f_app_setup(app_window)
    editor_window, editor_panel = f_make_panel(20, 111, 1, 3)

    cur_x, cur_y = editor_window.getyx()
    choices_window, choices_panel = f_make_panel(MAX_PREDICTIONS, 1, cur_y+2, cur_x+2)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    choices_window.bkgd(' ', curses.color_pair(1))
    choices_window.refresh()

    text = ''
    last_word = ''

    while 1:
        tab_position = 0
        user_char = app_window.getch()

        if user_char == curses.KEY_BACKSPACE: #Backspace
            if len(text) > 0:
                text = text[:-1]
        elif user_char == 9 or user_char == curses.KEY_STAB:
            tab_position = (tab_position + 1) % (MAX_PREDICTIONS + 1)
        else:
            text = text + str(chr(user_char))

        editor_window.clear()
        editor_window.addstr(3, 0, text)
        editor_window.refresh()


        #Display predictions
        if len(text) > 0 and text[-1] != ' ':
            first_word = ''
            second_word = ''
            word_array = text.split(' ')

            try:    first_word = word_array[-2]
            except: first_word = '0'

            try:    second_word = word_array[-1]
            except: second_word = '0'
            #Switch '0' to some type of return character that is not usually used?

            next_words = f_predictions(first_word, second_word, prediction_list)

            if len(next_words) > 0:
                if text.split(' ')[-1] != last_word:
                    cur_x, cur_y = editor_window.getyx()
                    choices_window.mvwin(cur_x+2, cur_y+4)

                choices_window.clear()
                word_lens = [12]
                for w in next_words:
                    word_lens.append(len(w[1])) 
                c_width = max(word_lens)

                choices_window.resize(MAX_PREDICTIONS, c_width)
                for index, word in enumerate(next_words):
                    choices_window.addstr(index, 0, word[0])

                choices_panel.show()
                choices_window.refresh(); editor_window.refresh(); app_window.refresh()
            else:
                choices_window.clear()
                choices_panel.hide()


    f_app_teardown()


### MAIN ###
if __name__ == '__main__':
   curses.wrapper(f_editor)
