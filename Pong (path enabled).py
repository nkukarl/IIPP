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
show_path_flag = False
ball_path = []

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = random.randrange(-3, -1)
    else:
        ball_vel[0] = random.randrange(-4, -2)
        ball_vel[1] = random.randrange(-3, -1)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_path  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    ball_path = []
 
def show_path():
    global show_path_flag, ball_path
    show_path_flag = not show_path_flag
    if show_path_flag:
        ball_path = []

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, ball_path, cnt
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if (ball_pos[1] <= paddle1_pos[1] - HALF_PAD_HEIGHT) or (ball_pos[1] >= paddle1_pos[1] + HALF_PAD_HEIGHT):
            score2 += 1
            spawn_ball(RIGHT)
            ball_path = []
        else:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
            
    if ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:
        if (ball_pos[1] <= paddle2_pos[1] - HALF_PAD_HEIGHT) or (ball_pos[1] >= paddle2_pos[1] + HALF_PAD_HEIGHT):
            score1 += 1
            spawn_ball(LEFT)
            ball_path = []
        else:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
    
    # draw path
    if show_path_flag:
        if [ball_pos[0], ball_pos[1]] not in ball_path:
            ball_path.append([ball_pos[0], ball_pos[1]])
        canvas.draw_polyline(ball_path, 2, "Green")
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    
    if paddle1_vel[1] > 0:
        if (paddle1_pos[1] + HALF_PAD_HEIGHT < HEIGHT - 1):
            paddle1_pos[1] += paddle1_vel[1]
    else:
        if paddle1_pos[1] - HALF_PAD_HEIGHT > 0:
            paddle1_pos[1] += paddle1_vel[1]

    paddle1_pos_up = paddle1_pos[1] - HALF_PAD_HEIGHT
    paddle1_pos_bottom = paddle1_pos[1] + HALF_PAD_HEIGHT
    
    if paddle2_vel[1] > 0:
        if (paddle2_pos[1] + HALF_PAD_HEIGHT < HEIGHT - 1):
            paddle2_pos[1] += paddle2_vel[1]
    else:
        if paddle2_pos[1] - HALF_PAD_HEIGHT > 0:
            paddle2_pos[1] += paddle2_vel[1]
    
    paddle2_pos_up = paddle2_pos[1] - HALF_PAD_HEIGHT
    paddle2_pos_bottom = paddle2_pos[1] + HALF_PAD_HEIGHT
    
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos_up), (PAD_WIDTH - 1,paddle1_pos_up), (PAD_WIDTH - 1, paddle1_pos_bottom), (0, paddle1_pos_bottom)], 1, "White", "White")
    canvas.draw_polygon([(WIDTH - PAD_WIDTH - 1, paddle2_pos_up), (WIDTH - 1, paddle2_pos_up), (WIDTH - 1, paddle2_pos_bottom), (WIDTH - PAD_WIDTH - 1, paddle2_pos_bottom)], 1, "White", "White")

    # draw scores
    canvas.draw_text(str(score1), [150, 50], 40, "White")
    canvas.draw_text(str(score2), [420, 50], 40, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    paddle_acc = 5
    if chr(key) == "W":
        paddle1_vel[1] += -paddle_acc
    elif chr(key) == "S":
        paddle1_vel[1] += paddle_acc
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] += -paddle_acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += paddle_acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == "W":
        paddle1_vel[1] = 0
    elif chr(key) == "S":
        paddle1_vel[1] = 0
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)
frame.add_button("Show path", show_path, 100)


# start frame
new_game()
frame.start()
