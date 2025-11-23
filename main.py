import keyboard
import file_manip
import os
from time import sleep
import msvcrt
import threading
import shutil
import pyautogui


INPUT_DELAY = 0.2 # these delays make it so that you don't just repeatedly detect the same keystroke
SEPERATOR = '~' * shutil.get_terminal_size().columns
MENU_TEXT = ['Hello! What would you like to do today?', 'Open Existing File <', 'Create New File', 'Exit']
display = MENU_TEXT
state = 0 # 0 = Home Screen
cursor_position = 1
external_editing = False

def flush_input_buffer():
    while msvcrt.kbhit():  # while characters are waiting
        msvcrt.getch()     # discard them

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def cursor_mover(key): # Checks if the key moves the cursor
    global display
    global cursor_position
    max_position = len(display) - 1
    if state == 0 or state == 1:
        min_position = 1
    else:
        min_position = 0
    if key == 'down':
        display[cursor_position] = display[cursor_position][:-2]
        cursor_position = min(max_position, cursor_position + 1)
        display[cursor_position] = display[cursor_position] + ' <'
        sleep(INPUT_DELAY)
    elif key == 'up':
        display[cursor_position] = display[cursor_position][:-2]
        cursor_position = max(min_position, cursor_position - 1)
        display[cursor_position] = display[cursor_position] + ' <'
        sleep(INPUT_DELAY)

def add_cursor_at(location):
    global display
    global cursor_position
    cursor_position = location
    display[location] = display[location] + ' <'

def simul_inputter_for_editing():
   global new_line
   global external_editing
   external_editing = True
   flush_input_buffer()
   new_line += input('Add to selected line: ')
   external_editing = False

def name_autofiller():
    sleep(0.1)
    pyautogui.write(current_file_name)

def editing_mode():
    global display
    global new_line
    while True:
        clear_terminal()
        print('\n'.join(display))
        print(f'{SEPERATOR}\nCurrently editing indicated line. Press Escape to stop.')
        new_line = display[cursor_position][:-2] # current line without cursor
        editing_key_pressed = keyboard.read_event().name
        if editing_key_pressed == 'backspace':
            new_line = new_line[:-1]
            sleep(INPUT_DELAY)
        elif editing_key_pressed == 'esc':
            break
        elif not external_editing: # lack of input delay because I want the key being pressed to instantly enter the input prompt
            threading.Thread(target=simul_inputter_for_editing).start()
            keyboard.wait('enter')
            sleep(INPUT_DELAY)
        display[cursor_position] = new_line + ' <'
    sleep(INPUT_DELAY)

while True:
    clear_terminal()
    print('\n'.join(display)) # Draws the screen!
   
    if state == 0: # Home Screen
        key_currently_pressed = keyboard.read_event().name # this statement makes it so the screen only refreshes upon a keystroke
        cursor_mover(key_currently_pressed)
        if key_currently_pressed == 'enter':
            if cursor_position == 1: # Open Existing File
                display = ['Select a File:'] + os.listdir('.') # loads current directory
                add_cursor_at(1)
                state = 1
            elif cursor_position == 2: # Create New File
                display = [''] # Creates the text of the empty file
                current_file_name = '' # Ensures there is no saved file name already
                add_cursor_at(0)
                state = 2
            elif cursor_position == 3:
                clear_terminal()
                exit()
            sleep(INPUT_DELAY)
    
    elif state == 1: # Finding A file State
        key_currently_pressed = keyboard.read_event().name # this statement makes it so the screen only refreshes upon a keystroke
        cursor_mover(key_currently_pressed)
        
        if key_currently_pressed == 'enter':
            current_file_name = display[cursor_position][:-2]
            display = file_manip.read_from_file(display[cursor_position][:-2])
            add_cursor_at(0)
            state = 2
            sleep(INPUT_DELAY)
    
    elif state == 2: # File Editing State
        print(f'{SEPERATOR}\nSelect a line to edit (e) or press s to save and exit. Press esc to exit without saving.')
        
        key_currently_pressed = keyboard.read_event().name # this statement makes it so the screen only refreshes upon a keystroke
        cursor_mover(key_currently_pressed)
        
        if key_currently_pressed == 'enter': # Add a new line
            display.insert(cursor_position + 1,'')
            sleep(INPUT_DELAY)
        elif key_currently_pressed == 's': # Saves
            clear_terminal()
            flush_input_buffer()
            threading.Thread(target=name_autofiller).start()
            name_given = input('Name File: ')
            print('Saving...')
            display[cursor_position] = display[cursor_position][:-2] # removes cursor from display
            file_manip.write_to_file(name_given, '\n'.join(display))
            print(f'Saved as {name_given}')
            sleep(1)
            display = MENU_TEXT
            state = 0
            add_cursor_at(1)
        elif key_currently_pressed == 'e':
            sleep(INPUT_DELAY)
            editing_mode()
        elif key_currently_pressed == 'esc':
            flush_input_buffer()
            if input(f'{SEPERATOR}\nAre you sure you want to exit WITHOUT saving? (y/n) ') == 'y': 
                display = MENU_TEXT
                state = 0
                add_cursor_at(1)
            sleep(INPUT_DELAY)
