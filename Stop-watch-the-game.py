# template for "Stopwatch: The Game"
import simplegui
# define global variables
t = 0
interval = 100
succ_stops = 0
total_stops = 0
running_state = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    BC = (t // 10) % 60
    A = t // 600
    return str(A) + ":" + str(BC) + "." + str(D)
   
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running_state
    timer.start()
    running_state = True

def stop():
    global succ_stops, total_stops, running_state
    if running_state:
        total_stops += 1
        if t % 10 == 0:
            succ_stops += 1
    timer.stop()
    running_state = False
    

def reset():
    global t, succ_stops, total_stops, running_state
    timer.stop()
    running_state = "False"
    t = 0
    succ_stops = 0
    total_stops = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global t
    t += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(t), [40, 100], 36, "red")
    canvas.draw_text(str(succ_stops) + "/" + str(total_stops), [130, 30], 36, "red")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
