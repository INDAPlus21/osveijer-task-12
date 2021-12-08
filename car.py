import pygame as pg
from math import acos, cos, sin, degrees

track = [pg.math.Vector2(100,100),pg.math.Vector2(250,50),pg.math.Vector2(400,150),pg.math.Vector2(700,25),pg.math.Vector2(900,400),pg.math.Vector2(800,600),pg.math.Vector2(500,750),pg.math.Vector2(100,700)]
track_width = 40
bollard_width = 48

pos = track[-1].lerp(track[0], 0.5)
vel = pg.math.Vector2(0,0)
max_vel = 20
max_grip = 3


corner_index = 0
target = pg.math.Vector2(0,0)
target_velocity = 0
#next_corner = []
#incorner_index = 0


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
    l2 = next_point - point
    v = abs(degrees(acos(l1.dot(l2)/(l1.magnitude()*l2.magnitude()))))
    tar_vel = (max_grip * v)/25
    corner_index += 1
    if corner_index == len(track):
        corner_index = 0
    return tar, tar_vel

def acceleration():
    global target,target_velocity,pos,vel,max_vel,max_grip,track_width
    desiered = target - pos
    if desiered.magnitude() <= track_width:
        target,target_velocity = get_target()
        return acceleration()
    else:
        braking_distance = track_width
        v = vel.magnitude()
        braking_distance += v
        while v > target_velocity:
            v -= max_grip
            braking_distance += v
        if desiered.magnitude() <= braking_distance:
            desiered.scale_to_length(target_velocity)
        else:
            desiered.scale_to_length(max_vel)
    accel = desiered - vel
    if accel.magnitude() > max_grip:
        accel.scale_to_length(max_grip)
    return accel
    

target,target_velocity = get_target()
while 1 == 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
    draw_bollard()
    draw_road()
    draw_car(pos)
    pg.display.flip()
    #get_next_corner(track,corner_index)
    vel += acceleration()
    pos += vel
    pg.time.wait(25)
    
    
