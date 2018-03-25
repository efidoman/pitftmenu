#!/usr/bin/python

import sys, pygame
from pygame.locals import *
import math,time
import subprocess
import os,requests,json,pprint,datetime
from time import gmtime, strftime

from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Initialize pygame and hide mouse
pygame.init()
pygame.mouse.set_visible(0)

def draw_arrow(screen, colour, start, end):
    arrowSize=9
    pygame.draw.line(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, colour, ((end[0]+arrowSize*math.sin(math.radians(rotation)), end[1]+arrowSize*math.cos(math.radians(rotation))), (end[0]+arrowSize*math.sin(math.radians(rotation-120)), end[1]+arrowSize*math.cos(math.radians(rotation-120))), (end[0]+arrowSize*math.sin(math.radians(rotation+120)), end[1]+arrowSize*math.cos(math.radians(rotation+120)))))

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    font=pygame.font.Font(None,32)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    pygame.draw.rect(screen, blue, (xpo-10,ypo-10,width,height),3)

# define function for printing text in a specific place with a specific colour
# returns rendered text width, height
def make_label(text, xpo, ypo, fontsize, colour):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    return font.size(str(text)) 

def update_dashboard():
    try:
        res1=requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/entries.json?count=1')
        d=res1.json()
        #pprint.pprint(d)
    except:
        print "failed request entries"
        return

    try:
        entryid=d[0]['_id']
        entrydate=d[0]['date']/1000 # convert from milliseconds to seconds
        bg=d[0]['glucose']
        unfiltered=d[0]['unfiltered']
        filtered=d[0]['filtered']
        direction=d[0]['direction']
        trend=d[0]['trend']
        noise=d[0]['noise']
        print 'entry id =',entryid,', direction=',direction,', noise=',noise
        print 'bg =',bg,', unfiltered=',unfiltered,', filtered=',filtered
    except:
        print "Glucose not found in response to get entries"
        return

    if update_dashboard.lastentryid == entryid:
        print "No change yet glucose entry"
#        return # need to update clock here
    else:
        update_dashboard.lastentryid=entryid


    try:
        res2 = requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/devicestatus?count=1')      
        data2=res2.json()
        pprint.pprint(data2)
    except:
        print "failed request devicestatus"
        return

    try:
        rigbattery=data2[0]['uploader']['battery']
        cob=data2[0]['openaps']['enacted']['COB']
        iob=data2[0]['openaps']['enacted']['IOB']
        tick=data2[0]['openaps']['enacted']['tick']
        enacttimestamp=data2[0]['openaps']['enacted']['timestamp']
        print 'enact timestamp =',enacttimestamp
        print 'tick =',tick
        print 'COB =',cob
        print 'IOB =',iob
        print 'rigbattery =',rigbattery
    except:
        print "Edison battery not found in response to get devicestatus"
        return
    

#timeHHMM=datetime.datetime.now()

   # timeHHMM=strftime("%H:%M", datetime.datetime.now())
    timeNow = datetime.datetime.now()
    epochdate = time.time()
    print "timeNow=",timeNow 
    print "entrydate=", entrydate
    print "epochdate=", epochdate
    timeHHMM = timeNow.strftime("%I:%M")
    minutesBG = (epochdate - entrydate)/60
    print "minutesBG=", minutesBG
    mins = "%.0f" % minutesBG + 'min'
    print "mins=", mins


    screen.fill(black)
    leftB=5
    topB=5
    spacingW=12
    spacingH=2

    # Testing
#    bg=343
#    trend=5
    # Ending Testing

    glucW, glucH = make_label(bg, leftB, topB, 100, fgColor)
    print "glucW =",glucW,"glucH =",glucH

    tickW, tickH = make_label(tick, leftB + glucW + spacingW, topB, 50, fgColor)

    startx = glucW + spacingW +25
    starty = tickH + 10 
    if trend == 1:
        #  direction='DoubleUp'
        draw_arrow(screen, fgColor, (startx,starty+20), (startx,starty))
        draw_arrow(screen, fgColor, (startx+25,starty+20), (startx+25,starty))
    if trend == 2:
        #  direction='SingleUp'
        draw_arrow(screen, fgColor, (startx+12,starty+20), (startx+12,starty))
    if trend == 3:
        #  direction='FortyFiveUp'
        draw_arrow(screen, fgColor, (startx,starty+20), (startx+30,starty))
    if trend == 4:
        #  direction='Flat'
        draw_arrow(screen, fgColor, (startx,starty+5), (startx+30,starty+5))
    if trend == 5:
        #  direction='FortyFiveDown'
        draw_arrow(screen, fgColor, (startx,starty), (startx+30,starty+20))
    if trend == 7:
        #  direction='DoubleDown'
        draw_arrow(screen, fgColor, (startx,starty), (startx,starty+20))
        draw_arrow(screen, fgColor, (startx+25,starty), (startx+25,starty+20))
    if trend == 6:
        #  direction='SingleDown'
        draw_arrow(screen, fgColor, (startx+12,starty), (startx+12,starty+20))

    w,h1 = make_label(timeHHMM, leftB + glucW + tickW + 2 * spacingW, topB, 60, fgColor)
    iobs = "%.1f" % iob + 'u'
    cobs = "%.0f" % cob + 'g'
#    iobs = str(iob) + 'U'
    
    w,h2 = make_label(mins, leftB + glucW + tickW + 2 * spacingW, topB + h1 + spacingH, 45, fgColor)

    bat = "%.0f" % rigbattery + '%'
  
    make_label(bat, leftB + glucW + tickW + 2 * spacingW, topB + h1 + h2 + spacingH, 45, fgColor)

    startx = leftB
    starty = topB + glucH + 0 #spacingH
    w,h = make_label(iobs, startx, starty, 80, fgColor)
    starty = starty + h
    w,h = make_label(cobs, startx, starty, 80, fgColor)
    pygame.display.update()

update_dashboard.lastentryid=''

# define function that checks for touch location
def on_touch():
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 30 <= touch_pos[0] <= 240 and 30 <= touch_pos[1] <=85:
            button(1)
    # button 2 event
    if 260 <= touch_pos[0] <= 470 and 30 <= touch_pos[1] <=85:
            button(2)
    # button 3 event
    if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
            button(3)
    # button 4 event
    if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
            button(4)
    # button 5 event
    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
            button(5)
    # button 6 event
    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
            button(6)
    # button 7 event
    if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
            button(7)
    # button 8 event
    if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
            button(8)

# Define each button press action
def button(number):
    print "You pressed button ",number

    if number == 1:
        time.sleep(5) #do something interesting here

    if number == 2:
        time.sleep(5) #do something interesting here

    if number == 3:
        time.sleep(5) #do something interesting here

    if number == 4:
        time.sleep(5) #do something interesting here

    if number == 5:
        time.sleep(5) #do something interesting here

    if number == 6:
        time.sleep(5) #do something interesting here

    if number == 7:
        time.sleep(5) #do something interesting here

    if number == 8:
        time.sleep(5) #do something interesting here

#colors     R    G    B
white   = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)
black   = (  0,   0,   0)
cyan    = ( 50, 255, 255)
magenta = (255,   0, 255)
yellow  = (255, 255,   0)
orange  = (255, 127,   0)
fgColor = ( 30,  80,  80)

# Set up the base menu you can customize your menu with the colors above

#set size of the screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

# Background Color
screen.fill(black)

# Outer Border
#pygame.draw.rect(screen, blue, (0,0,320,240),10)

#res1=requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/entries.json?count=1')
#d=res1.json()
#pprint.pprint(d)
#print d

#glucose=0
#if len(d) > 0:
#    if 'glucose' in d[0]:
#        glucose=d[0]['glucose']


#res2 = requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/devicestatus?count=1')
#data2=res2.json()
#pprint.pprint(data2)



# Buttons and labels
# First Row
#make_button("Menu Item 2", 260, 30, 55, 210, fgColor)
# Second Row
make_label("Eric 3", 30, 105, 28, fgColor)
#make_button("Menu item 4", 260, 105, 55, 210, fgColor)
# Third Row
make_label("Eric 5", 30, 180, 28, fgColor)
#make_button("Menu item 6", 260, 180, 55, 210, fgColor)
# Fourth Row
# make_button("Menu item 7", 30, 255, 55, 210, fgColor)
# make_button("Menu item 8", 260, 255, 55, 210, fgColor)

# While loop to manage touch screen inputs
counter=600
loops=0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print "screen pressed" #for debugging purposes
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            print pos #for checking
            pygame.draw.circle(screen, white, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
            sys.exit()
            on_touch()

#ensure there is always a safe way to end the program if the touch screen fails

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    if counter >= 600:
        counter = 0
        update_dashboard()
        loops = loops + 1

    pygame.time.wait(100)
    counter=counter+1





