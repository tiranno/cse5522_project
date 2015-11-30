#!/usr/bin/python3
from time import sleep
import os
import curses, curses.panel
import sys
import csv
from operator import itemgetter

MAX_PREDICTIONS = 3

### KNOWN ISSUES ###
# * Crashes on moving panel beyond bounds of terminal
# * No higlighting of selected term yet
# * Not showing cursor position / moving back up windows between typing
###


# Read in the CPT data resultant of training, return it as an array
def f_import_predictions():
    prediction_list = []
    with open('generated_cpt.csv', 'r') as f:
        reader = csv.reader(f)
        prediction_list = list(reader)
    return prediction_list

# Returns a list of predictions dependent on the previous two words (it there were any)
def f_predictions(word_one, word_two, prediction_list):
    words = []
    for line in prediction_list:
        if line[1] == word_one and line[2] == word_two:
            word = line[-1]
            probability = line[0]
            words.append([word, probability])

    final = []
    if len(words) > 0:
        sorted_words = sorted(words, key=itemgetter(1), reverse=True)
        for word in sorted_words:
            if len(final) == MAX_PREDICTIONS:
                break
            final.append(word)
    return final

# Display/hide/change the panel associated with the predictions
def f_display_predictions(next_words, text, choices_win, choices_pan, editor_win, app_win):
    if len(next_words) > 0:
        # if text.split(' ')[-1] != last_word:
        cur_x, cur_y = editor_win.getyx()
        choices_win.mvwin(cur_x+2, cur_y+4)

        choices_win.clear()
        word_lens = [12]
        for w in next_words:
            word_lens.append(len(w[1]))
        c_width = max(word_lens)

        choices_win.resize(MAX_PREDICTIONS, c_width)
        for index, word in enumerate(next_words):
            choices_win.addstr(index, 0, word[0])

        choices_win.refresh(); editor_win.refresh(); app_win.refresh()
        choices_pan.show()
    else:
        next_words = []
        choices_win.clear()
        choices_pan.hide()

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
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)

    prediction_list = f_import_predictions()

    f_app_setup(app_window)
    editor_window, editor_panel = f_make_panel(20, 111, 1, 3)

    cur_x, cur_y = editor_window.getyx()
    choices_window, choices_panel = f_make_panel(MAX_PREDICTIONS, 1, cur_y+2, cur_x+2)
    choices_window.bkgd(' ', curses.color_pair(1))
    choices_window.refresh()

    text = ''
    last_word = ''
    next_words = []
    tab_position = 0

    while 1:
        user_char = app_window.getch()

        #BACKSPACE input
        if user_char == curses.KEY_BACKSPACE:
            if len(text) > 0:
                text = text[:-1]
            tab_position = 0
        #TAB input
        elif user_char == 9 or user_char == curses.KEY_STAB:
            if len(next_words) > 0:
                tab_position = (tab_position + 1) % (len(next_words) + 1)
            else:
                text = text + '\t'
        #ENTER input
        elif user_char == 10 or user_char == curses.KEY_ENTER:
            if tab_position > 0:
                text = text + " " + next_words[tab_position - 1][0]
                tab_position = 0
                enter = 1
            else:
                text = text + '\n'
        #TODO: control inputs. ^C is quit, ^S save to text file
        #Put character in text
        else:
            text = text + str(chr(user_char))
            tab_position = 0

        editor_window.clear()
        editor_window.addstr(3, 0, text)
        editor_window.refresh()


        #Display predictions (put into own function)
        if len(text) > 0 and text[-1] != ' ' and text[-1] != '\n':
            first_word = ''
            second_word = ''
            word_array = text.rstrip(' ').split(' ')

            try:    first_word = word_array[-2].lower()
            except: first_word = '0'

            try:    second_word = word_array[-1].lower()
            except: second_word = '0'

            if "." not in second_word:
                if "." in first_word:
                    first_word = '0'
                next_words = f_predictions(first_word, second_word, prediction_list)
                f_display_predictions(next_words, text, choices_window, choices_panel, editor_window, app_window)

            #Switch '0' to some type of return character that is not usually used?
            #take care of special cases: newline, end of sentence, etc.

    f_app_teardown()


### MAIN ###
if __name__ == '__main__':
   curses.wrapper(f_editor)
