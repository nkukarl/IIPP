# template for "Stopwatch: The Game"
import simplegui
# define global variables
t = 0
interval = 100
running_state = False
lapped_time = []

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
    if running_state:
        lapped_time.append(format(t))

# define event handler for timer with 0.1 sec interval
def tick():
    global t
    t += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(t), [40, 40], 30, "red")
    lapped_head = 100
    for i in range(len(lapped_time)):
        canvas.draw_text(format_id(i + 1), [10, lapped_head], 30, "white")
        canvas.draw_text(lapped_time[i], [80, lapped_head], 30, "white")
        lapped_head += 30

# create frame
frame = simplegui.create_frame("Stopwatch", 200, 975)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.add_button("Lap", lap, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
