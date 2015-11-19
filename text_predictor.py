#!/usr/bin/python3
import os
import curses
import signal
import sys

MAX_PREDICTIONS = 3

def f_app_setup ():
    app_window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    app_window.keypad(1)
    app_window.border(1)
    # Header and information
    app_window.addstr(0,2," TEXT PREDICTOR  |  Help: [!!!] ")
    app_window.addstr(1,5,"Enter your text below")
    return app_window

def f_app_teardown (app_window):
    app_window.border(0)
    app_window.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def f_new_subwindow (parent, begin_x, begin_y, height, width):
    # window = panel.new_panel(parent)
    window = parent.derwin(height, width, begin_y, begin_x)
    window.refresh()
    return window

def f_display_predictions (parent, selected_pos, current_string):
    coord_tuple = curses.getsyx()
    #Gather posibilies
    words = ['Hello', 'World', "Tiranno"]
    #max_width = [max length of longest word to return]
    # Display posibilities
    cur_len = len(current_string)
    max_width = len(max(words, key=len))
    win = f_new_subwindow(parent, coord_tuple[0]-cur_len, coord_tuple[1]-cur_len, MAX_PREDICTIONS, max_width)
    for index, w in enumerate(words):
        win.addstr(index,0, w)
    win.refresh()


app_window = f_app_setup() # Main app
text_window = f_new_subwindow(app_window, 5, 2, 20, 100) # Text editor window

text_file = ''
while 1:
    tab_position = 0

    user_char = app_window.getch()

    if user_char == curses.KEY_BACKSPACE: #Backspace
        if len(text_file) > 0:
            text_file = text_file[:-1]
    elif user_char == 9 or user_char == curses.KEY_STAB:
        tab_position = (tab_position + 1) % (MAX_PREDICTIONS + 1)
    else:
        text_file = text_file + str(chr(user_char))

    text_window.clear()
    text_window.addstr(2,0, text_file)
    text_window.refresh()

    if len(text_file) > 0 and text_file[-1] != ' ':
        last_string = text_file.split(' ')[-1]
        # prediction_window = f_display_predictions(text_window, tab_position, last_string)


f_app_teardown(app_window)
