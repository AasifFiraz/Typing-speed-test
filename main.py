import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Typing Speed Test!")
	stdscr.addstr("\nPress any key to start! ")
	stdscr.refresh()
	stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)
	stdscr.addstr(2, 0, f"WPM: {wpm}", curses.color_pair(1))

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
            # Shows red color if the text entered is wrong
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)

def load_sentence():
	with open("words.txt", "r") as sentences:
		lines = sentences.readlines()
        
        # randomely select a sentence for the user to type   
		return random.choice(lines).strip()

def wpm_test(stdscr):
	target_text = load_sentence()
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)

	while True:
		time_gone = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_gone / 60)) / 5) # round function to get a whole number

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

        # Converting the list to a string to check if the user has completed typing all words   
		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

        # try and except is used to make sure the program does not crash if user does not a enter a key    
		try:
			key = stdscr.getkey()
   
		except:
			continue

		if ord(key) == 27:
			break
        
		if ord(key) == 8:
			if len(current_text) > 0:
				current_text.pop()
                
              
        # cannot add more texts than the len of the text    
		elif len(current_text) < len(target_text):
			current_text.append(key)
   
        
def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
    # If user press any key other than esc he can play again
	while True:
		wpm_test(stdscr)
		stdscr.addstr(3, 0, "Congrats ! You completed the text! Press Esc to Quit, any key to play again... ")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)