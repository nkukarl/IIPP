# Modification of pong: Squash

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
bounce_record = 0
paddle_color = "White"

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, bounces
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(4, 8)
        ball_vel[1] = random.randrange(-6, -2)
        #ball_vel[0] = random.randrange(2, 4)
        #ball_vel[1] = random.randrange(-3, -1)
    else:
        ball_vel[0] = random.randrange(-4, -2)
        ball_vel[1] = random.randrange(-3, -1)
    bounces = 0

# define event handlers
def new_game():
    global paddle_pos, paddle_vel # these are numbers
    paddle_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle_vel = [0, 0]
    spawn_ball(RIGHT)

def draw(canvas):
    global paddle_pos, ball_pos, ball_vel, bounces, bounce_record, paddle_color
        
    # draw mid line and gutters
    #canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    #canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS):
        ball_vel[0] = - ball_vel[0]
        paddle_color = "White"
    
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
        paddle_color = "White"
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if (ball_pos[1] <= paddle_pos[1] - HALF_PAD_HEIGHT) or (ball_pos[1] >= paddle_pos[1] + HALF_PAD_HEIGHT):
            paddle_color = "Red"
            spawn_ball(RIGHT)
        else:
            paddle_color = "Green"
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
            bounces += 1
            if bounces > bounce_record:
                bounce_record = bounces
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    
    if paddle_vel[1] > 0:
        if (paddle_pos[1] + HALF_PAD_HEIGHT < HEIGHT - 1):
            paddle_pos[1] += paddle_vel[1]
    else:
        if paddle_pos[1] - HALF_PAD_HEIGHT > 0:
            paddle_pos[1] += paddle_vel[1]

    paddle_pos_up = paddle_pos[1] - HALF_PAD_HEIGHT
    paddle_pos_bottom = paddle_pos[1] + HALF_PAD_HEIGHT
    
    # draw paddles
    canvas.draw_polygon([(0, paddle_pos_up), (PAD_WIDTH - 1,paddle_pos_up), (PAD_WIDTH - 1, paddle_pos_bottom), (0, paddle_pos_bottom)], 1, paddle_color, paddle_color)
    
    # draw number of bounces
    canvas.draw_text(str(bounces) + " bounce(s)", [30, 30], 20, "White")
    canvas.draw_text("Bounce record: " + str(bounce_record), [30, 50], 20, "Red")
    
def keydown(key):
    global paddle_vel, BALL_RADIUS
    paddle_acc = 5
    if key == simplegui.KEY_MAP["up"]:
        paddle_vel[1] += -paddle_acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle_vel[1] += paddle_acc
    elif key == simplegui.KEY_MAP["left"]:
        if BALL_RADIUS - 5 > 0:
            BALL_RADIUS -= 5
    elif key == simplegui.KEY_MAP["right"]:
        if BALL_RADIUS + 5 <= 40:
            BALL_RADIUS += 5
   
def keyup(key):
    global paddle_vel
  
    if key == simplegui.KEY_MAP["up"]:
        paddle_vel[1] = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)
frame.add_label("Press left or right arrow to decrease or increase ball size", 100)


# start frame
new_game()
frame.start()
