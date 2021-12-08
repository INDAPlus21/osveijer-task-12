import pygame as pg
from math import acos, cos, sin, degrees, copysign

track = [pg.math.Vector2(100,100),pg.math.Vector2(250,50),pg.math.Vector2(300,150),pg.math.Vector2(400,50),pg.math.Vector2(700,25),pg.math.Vector2(900,400),pg.math.Vector2(800,600),pg.math.Vector2(500,750),pg.math.Vector2(100,700)]
track_width = 40
bollard_width = 48

pos = track[-1].lerp(track[0], 0.5)
vel = pg.math.Vector2(0,0)
max_vel = 7
max_grip = 0.3


corner_index = 0
target = pg.math.Vector2(0,0)
target_velocity = 0
turn_in = 0


pg.init()

size = width, height = 1000, 800

screen = pg.display.set_mode(size)

def draw_road():
    global track,track_width
    pg.draw.lines(screen,(100,100,100),True,track,track_width)
    for i in track:
        pg.draw.circle(screen,(100,100,100),i,track_width/2)

def draw_bollard():
    global track,bollard_width
    pg.draw.lines(screen,(255,0,0),True,track,bollard_width)
    for i in track:
        pg.draw.circle(screen,(255,0,0),i,bollard_width/2)
            
def draw_car(pos):
    pg.draw.circle(screen, (0,255,0), pos, 3)
    
def get_target():
    global corner_index, track
    tar = track[corner_index]
    point = track[corner_index]
    if corner_index == len(track) - 1:
        previous_point = track[corner_index-1]
        next_point = track[0]
    else:
        previous_point = track[corner_index-1]
        next_point = track[corner_index+1]
    l1 = previous_point - point
    l1n = pg.math.Vector2(l1.y, -l1.x).normalize()
    l2 = next_point - point
    v = degrees(acos(l1.dot(l2)/(l1.magnitude()*l2.magnitude())))
    # check if corner is clockwise or counter clockwise using determinant of a matrix made of the two vectors
    corner_dir = copysign(1,(l1.x*l2.y-l2.x*l1.y))
    # set target to the outside of the track to follow the racing line
    tar = ((l1n * (corner_dir) * track_width) / 2) + track[corner_index]
    # calculte the target velocity at corner entry using the grip and the corner angle
    tar_vel = (max_grip * v)/8
    # calculte the turn-in point using the width of the track and the corner angle
    turn_in = track_width * (v / 90) * 1.4
    corner_index += 1
    if corner_index == len(track):
        corner_index = 0
    return tar, tar_vel, turn_in

def calculate_acceleration(pos,vel,max_vel,max_grip,track_width):
    global target,target_velocity,turn_in
    desiered = target - pos
    # if at or past turn-in point switch target to next corner
    if desiered.magnitude() <= turn_in:
        target,target_velocity,turn_in = get_target()
        return calculate_acceleration(pos,vel,max_vel,max_grip,track_width)
    else:
        # if within braking zone, desiere the velocity to be the target_velocity
        braking_distance = calculate_braking_distance(vel,turn_in)
        if desiered.magnitude() <= braking_distance:
            desiered.scale_to_length(target_velocity)
        # if just driving make sure car can't exceed it's top speed
        else:
            if desiered.magnitude() > max_vel:
                desiered.scale_to_length(max_vel)
    accel = desiered - vel
    if accel.magnitude() > max_grip:
        accel.scale_to_length(max_grip)
    return accel
    

def calculate_braking_distance(vel,turn_in):
    braking_distance = turn_in
    v = vel.magnitude()
    braking_distance += v
    while v > target_velocity:
        v -= max_grip
        braking_distance += v
    return braking_distance


target,target_velocity,turn_in = get_target()
while 1 == 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
    draw_bollard()
    draw_road()
    vel += calculate_acceleration(pos,vel,max_vel,max_grip,track_width)
    pos += vel
    draw_car(pos)
    pg.display.flip()
    pg.time.wait(10)
    
    
