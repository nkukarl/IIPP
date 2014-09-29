# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

rng = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global guess_remain, secret_number
    
    guess_remain = int(math.ceil(math.log(rng) / math.log(2)))
    secret_number = random.randrange(0, rng)
    print "New game. Range is from 0 to", rng
    print "Number of remaining guesses is", guess_remain, "\n"
    

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global rng
    rng = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global rng
    rng = 1000
    new_game()
    
def input_guess(guess):
    global guess_remain, secret_number
    
    print "Guess was ", int(guess)
    
    guess_remain -= 1
    print "Number of remaining guesses is", guess_remain
    
    if guess_remain > 0:
        if int(guess) > secret_number:
            print "Lower!\n"
        elif int(guess) < secret_number:
            print "Higher!\n"
        else:
            print "Correct!\n"
            new_game()
    elif int(guess) == secret_number:
        print "Correct!\n"
        new_game()
    else:
        print "You ran out of guesses. The number was", secret_number, "\n"
        new_game()

    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
