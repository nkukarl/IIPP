# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, exposed, state, turn
    deck = range(8)
    deck.extend(deck)
    random.shuffle(deck)
    exposed = [0] * len(deck)
    state = 0
    turn = 0
    label.set_text("Turns = " + str(turn))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, idx1, idx2, turn
    if state == 0:
        if exposed[pos[0] // 50 + pos[1] // 100 * 4] == 0:
            idx1 = pos[0] // 50 + pos[1] // 100 * 4
            exposed[idx1] = 1
            state = 1
    elif state == 1:
        if exposed[pos[0] // 50 + pos[1] // 100 * 4] == 0:
            idx2 = pos[0] // 50 + pos[1] // 100 * 4
            exposed[idx2] = 1
            state = 2
            turn += 1
            label.set_text("Turns = " + str(turn))
    else:
        if exposed[pos[0] // 50 + pos[1] // 100 * 4] == 0:
            if deck[idx1] != deck[idx2]:
                    exposed[idx1] = 0
                    exposed[idx2] = 0
            idx1 = pos[0] // 50 + pos[1] // 100 * 4
            exposed[idx1] = 1
            state = 1
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    i = 0
    for j in range(4):
        for k in range(4):
            if exposed[i]:
                canvas.draw_text(str(deck[i]), [50 * k + 15, 100 * j + 65], 40, "white")
            else:
                canvas.draw_polygon([[50 * k, 100 * j], [50 * (k + 1), 100 * j], [50 * (k + 1), 100 * (j + 1)], [50 * k, 100 * (j + 1)]], 3, 'Red', 'Green')
            i += 1
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 200, 400)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
