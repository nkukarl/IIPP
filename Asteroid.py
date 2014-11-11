# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
#score = 0
#lives = 3
time = 0.5
started = False
#thrust_on = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, angle_vel, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if thrust_on:
            canvas.draw_image(self.image, (self.image_center[0] + 90, self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()

    def update(self):
        self.angle += self.angle_vel
        self.forward_vector = angle_to_vector(self.angle)
        if thrust_on:
            self.vel[0] += self.forward_vector[0] * 0.5
            self.vel[1] += self.forward_vector[1] * 0.5
        self.vel[0] *= 0.97
        self.vel[1] *= 0.97
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
    
    def shoot(self):
        global missile_group
        a_missile = Sprite([my_ship.pos[0] + my_ship.radius * math.cos(my_ship.angle), my_ship.pos[1] + my_ship.radius * math.sin(my_ship.angle)], [my_ship.vel[0] + my_ship.forward_vector[0] * 5, my_ship.vel[1] + my_ship.forward_vector[1] * 5], 0, 0, missile_image, missile_info, missile_sound)            
        missile_group.add(a_missile)
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, angle, angle_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound and started:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        if dist(self.pos, other_object.get_pos()) < self.radius + other_object.get_radius():
            return True
        else:
            return False

           
def draw(canvas):
    global time, lives, score, started, thrust_on, rock_group, missile_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if started and lives > 0:

        # draw ship and sprites
        my_ship.draw(canvas)
        
        # update ship and sprites
        my_ship.update()
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        
        # score and lives
        canvas.draw_text('Lives: ' + str(lives), (20, 30), 20, 'White')
        canvas.draw_text('Score: ' + str(score), (WIDTH - 120, 30), 20, 'White')        
    
        if group_collide(rock_group, my_ship):
            lives -= 1
        score += group_group_collide(rock_group, missile_group)
        
    else:
        rock_group = set([])
        missile_group = set([])
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size())
        started = False
        thrust_on = False
        ship_thrust_sound.rewind()
        soundtrack.rewind()
        
# keydown and keyup handler

def keydown(key):
    global thrust_on
    if key == simplegui.KEY_MAP['up']:
        thrust_on = True
    elif key == simplegui.KEY_MAP['right'] and started:
        my_ship.angle_vel += 0.1
    elif key == simplegui.KEY_MAP['left'] and started:
        my_ship.angle_vel -= 0.1
    elif key == simplegui.KEY_MAP['space'] and started:
        my_ship.shoot()

def keyup(key):
    global thrust_on
    if key == simplegui.KEY_MAP['up']:
        thrust_on = False
    elif key == simplegui.KEY_MAP['right'] and started:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['left'] and started:
        my_ship.angle_vel = 0

def mouse(pos):
    if(not started):
        new_game()
        
def group_collide(group, other_object):
    for item in set(group):
        if item.collide(other_object):
            group.remove(item)
            return True

def group_group_collide(group1, group2):
    cnt = 0
    for item in set(group1):
        if group_collide(group2, item):
            group1.remove(item)
            cnt += 1
    return cnt

def process_sprite_group(group, canvas):
    for item in set(group):
        item.draw(canvas)
        #item.update()
        if item.update():
            group.remove(item)
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if started:
        if len(rock_group) < 12:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [random.randrange(-100, 100) / 100.0, random.randrange(-100, 100) / 100.0]
            rock_angle = random.randrange(0, 10) / 100.0
            rock_angle_vel = random.randrange(-10, 10) / 100.0
            a_rock = Sprite(rock_pos, rock_vel, rock_angle, rock_angle_vel, asteroid_image, asteroid_info)
            if dist(a_rock.get_pos(), my_ship.get_pos()) >  (a_rock.get_radius() + my_ship.get_radius()) * 2:
                rock_group.add(a_rock)
        
# new_game
def new_game():
    global my_ship, rock_group, missile_group, score, lives, thrust_on, time, started
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, 0, ship_image, ship_info)
    rock_group = set([])
    missile_group = set([])
    score = 0
    lives = 3
    thrust_on = False
    time = 0.5
    started = True
    soundtrack.play()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
      
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse)

timer = simplegui.create_timer(1000.0, rock_spawner)
#new_game()

# get things rolling
timer.start()
frame.start()
