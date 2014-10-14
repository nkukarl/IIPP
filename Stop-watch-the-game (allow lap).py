# template for "Stopwatch: The Game"
import simplegui
# define global variables
t = 0
interval = 100
running_state = False
lapped_time = []
lapped_head_pos = 30
max_laps = 15
WIDTH = 500
HEIGHT = 300

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = str(t % 10)
    BC = str((t // 10) % 60)
    if len(BC) == 1:
        BC = '0' + BC
    A = str(t // 600)
    
    return A + ":" + BC + "." + D

def format_id(i):
    if len(lapped_time) < 10:
        return '#' + str(i)
    elif len(lapped_time) < 100:
        if len(str(i)) == 1:
            return '#0' + str(i)
        else:
            return '#' + str(i)
   
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running_state
    timer.start()
    running_state = True

def stop():
    global running_state
    timer.stop()
    running_state = False
    

def reset():
    global t, running_state, lapped_time
    timer.stop()
    running_state = False
    t = 0
    lapped_time = []
    
def lap():
    global lapped_time
    if running_state and len(lapped_time) < max_laps:        
        lapped_time.append(format(t))

# define event handler for timer with 0.1 sec interval
def tick():
    global t
    t += 1

# define draw handler
def draw(canvas):
    global lapped_head_pos
    canvas.draw_text(format(t), [30, 30], 30, "red")
    for i in range(min(len(lapped_time), max_laps)):
        canvas.draw_text(format_id(i + 1), [200, lapped_head_pos + 30 * i], 30, "white")
        canvas.draw_text(lapped_time[i], [280, lapped_head_pos  + 30 * i], 30, "white")

def key_down(key):
    global vel, lapped_head_pos
    if key == simplegui.KEY_MAP['down']:
        if lapped_head_pos + 30 * (len(lapped_time) - 1)  > HEIGHT:
            lapped_head_pos -= 30
    elif key == simplegui.KEY_MAP['up']:
        if lapped_head_pos < 30:
            lapped_head_pos += 30
        
# create frame
frame = simplegui.create_frame("Stopwatch", WIDTH, HEIGHT)

# register event handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)

timer = simplegui.create_timer(interval, tick)

frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.add_button("Lap", lap, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
