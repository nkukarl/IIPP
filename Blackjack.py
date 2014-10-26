# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
msg = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        self.hand_str = 'Hand contains'

    def __str__(self):
        return self.hand_str

    def add_card(self, card):
        self.hand.append(card)
        self.hand_str += ' ' + str(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for i in self.hand:
            value += VALUES[i.rank]
        if 'A' in self.hand_str:
            if value <= 11:
                value += 10
        return value
   
    def draw(self, canvas, pos):
        for i in range(min(5, len(self.hand))):
        #for i in range(len(self.hand)):
            self.hand[i].draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(i + j)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        temp = self.deck.pop()
        return Card(temp[0], temp[1])
    
    def __str__(self):
        return 'Deck contains ' + ' '.join(self.deck)      


#define event handlers for buttons
def deal():
    global outcome, in_play, dk, pl_hand, dl_hand, score, msg
    if in_play:
        msg = ''
        score -= 1
        #print outcome
        #print score
        in_play = False
    if not in_play:
        dk = Deck()
        dk.shuffle()
        pl_hand = Hand()
        dl_hand = Hand()
        pl_hand.add_card(dk.deal_card())
        #print 'player: ', pl_hand, 'value: ', pl_hand.get_value()
        dl_hand.add_card(dk.deal_card())
        #print 'dealer: ', dl_hand, 'value: ', dl_hand.get_value()
        pl_hand.add_card(dk.deal_card())
        #print 'player: ', pl_hand, 'value: ', pl_hand.get_value()
        dl_hand.add_card(dk.deal_card())
        #print 'dealer: ', dl_hand, 'value: ', dl_hand.get_value()
        in_play = True
        outcome = ''
        msg = "Hit or stand?"

def hit():
    # if the hand is in play, hit the player
    global dk, pl_hand, outcome, score, in_play, msg
    if in_play:
        if pl_hand.get_value() <= 21:
            pl_hand.add_card(dk.deal_card())
            #print 'player: ', pl_hand, 'value: ', pl_hand.get_value()
        if pl_hand.get_value() > 21:
            outcome = "You have busted, dealer wins!"
            score -= 1
            #print outcome
            #print score
            in_play = False
            msg = "New deal?"
        else:
            msg = "Hit or stand?"
       
def stand():
    global dk, dl_hand, outcome, score, in_play, msg
    if in_play:
        while dl_hand.get_value() < 17:
                dl_hand.add_card(dk.deal_card())
                #print 'dealer: ', dl_hand, 'value: ', dl_hand.get_value()
        if pl_hand.get_value() > dl_hand.get_value():
            outcome = "You win!"
            score += 1
        elif dl_hand.get_value() > 21:
            outcome = "Dealer has busted, you win!"
            score += 1
        elif pl_hand.get_value() == dl_hand.get_value():
            outcome = "Tie, dealer wins!"
            score -= 1
        else:
            outcome = "Dealer wins!"
            score -= 1
        #print outcome
        #print score
        msg = "New deal?"
        in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [100, 50], 50, "Black")
    canvas.draw_text("Player: " + str(pl_hand.get_value()), [100, 100], 30, "Black")
    pl_hand.draw(canvas, [100, 120])
    if in_play:
        canvas.draw_text("Dealer", [100, 250], 30, "Black")
        dl_hand.draw(canvas, [100, 270])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_CENTER[0], 270 + CARD_CENTER[1]], CARD_BACK_SIZE)
    else:
        canvas.draw_text("Dealer: " + str(dl_hand.get_value()), [100, 250], 30, "Black")
        dl_hand.draw(canvas, [100, 270])
    canvas.draw_text("Score: " + str(score), [100, 410], 30, "Red")
    canvas.draw_text(outcome, [100, 450], 30, "Blue")
    canvas.draw_text(msg, [100, 490], 30, "Blue")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
