import picounicorn
from machine import ADC, Pin

import time
import random

picounicorn.init()








# Main loop

w = picounicorn.get_width()
h = picounicorn.get_height()

def clearDisplay():
   # except for the lines where the button labels are

    for x in range(1,w-1):
        for y in range(h):
            picounicorn.set_pixel(x, y, 0, 0, 0)

def LineButton( b, cr, cg, cb ):
    if b == "A" :
       x = 0
       y = 0

    if b == "B" :
       x = 0
       y = 4

    if b == "X" :
       x = 15
       y = 0

    if b == "Y" :
       x= 15
       y = 4


    picounicorn.set_pixel(x, y, cr, cg, cb )
    picounicorn.set_pixel(x, y + 1, cr, cg, cb )
    picounicorn.set_pixel(x, y + 2, cr, cg, cb )

def NoButton( b ) :
    LineButton(b, 0, 0, 0 )

def LightButton( b ) :
    LineButton(b, 128, 128, 128 )

def OKButton( b ):

    LineButton(b, 0, 255, 0 )
#    if b == "A" :
#       x = 0
#       y = 0
#
#    if b == "B" :
#       x = 0
#       y = 5
#
#    if b == "X" :
#       x = 15
#       y = 0
#
#    if b == "Y" :
#       x= 15
#       y = 5
#
#
#    picounicorn.set_pixel(x, y, 0, 255, 0 )
#    picounicorn.set_pixel(x, y + 1, 0, 255, 0 )
#    picounicorn.set_pixel(x, y + 2, 0, 255, 0 )
        

def CancelButton( b ) :
    LineButton(b, 255, 0, 0 )
#    if b == "A" :
#       x = 0
#       y = 0
#
#    if b == "B" :
#       x = 0
#       y = 4
#
#    if b == "X" :
#       x = 15
#       y = 0
#
#    if b == "Y" :
#       x= 15
#       y = 4
#
#
#    picounicorn.set_pixel(x, y, 255, 0, 0 )
#    picounicorn.set_pixel(x, y + 1, 255, 0, 0 )
#    picounicorn.set_pixel(x, y + 2, 255, 0, 0 )

def RightButton( b ) :
    if b == "A" :
       x = 1
       y = 0

    if b == "B" :
       x = 1
       y = 4

    if b == "X" :
       x = 14
       y = 0

    if b == "Y" :
       x= 14
       y = 5


    picounicorn.set_pixel(x, y, 255, 255, 255)
    picounicorn.set_pixel(x - 1, y + 1, 255, 255, 255 )
    picounicorn.set_pixel(x , y + 1, 255, 255, 255 )
    picounicorn.set_pixel(x + 1, y + 1, 255, 255, 255 )

def LeftButton( b ) :
    if b == "A" :
       x = 1
       y = 0

    if b == "B" :
       x = 1
       y = 4

    if b == "X" :
       x = 14
       y = 0

    if b == "Y" :
       x= 14
       y = 5


    picounicorn.set_pixel(x - 1, y , 255, 255, 255 )
    picounicorn.set_pixel(x , y , 255, 255, 255 )
    picounicorn.set_pixel(x + 1, y, 255, 255, 255 )
    picounicorn.set_pixel(x, y +1 , 255, 255, 255)

def displayBattery() :

    vsys = ADC(29)                      # reads the system input voltage
    charging = Pin(24, Pin.IN)          # reading GP24 tells us whether or not USB power is connected
    conversion_factor = 3 * 3.3 / 65535

    full_battery = 4.2                  # reference voltages for a full/empty battery, in volts
    empty_battery = 2.8                 # the values could vary by battery size/manufacturer so you might need to adjust them


    voltage = vsys.read_u16() * conversion_factor
    percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100

    # draw a green box for the battery level
    for x in range( 10 ) :
        if ( x / 2 == int( x / 2 ) ) :
            picounicorn.set_pixel(2 + x, 1, 128, 128, 128 )
        if ( x * 10 <= percentage ) :
            picounicorn.set_pixel(2 + x, 4, 0, 255, 0 )
            picounicorn.set_pixel(2 + x, 5, 0, 255, 0 )

    if charging.value() == 1:         # if it's plugged into USB power...
        print("Charging!")

    print( voltage )
    print( percentage)

    
# block defs

tetrisblocks = [  \
             [ 0, 1, 0, 0, 1, 0, 0, 1, 1 ], \
             [ 1, 1, 1, 1, 1, 0, 1, 0, 0 ], \
             [ 1, 1, 0, 1, 0, 0, 1, 1, 0 ], \
             [ 1, 1, 1, 1, 0, 0, 1, 1, 1 ], \
             [ 0, 1, 0, 0, 1, 1, 0, 1, 0 ], \
             [ 0,1,0,0,1,0, 0,1,0], \
             [ 0,1,0, 0,1,0, 0,0,0], \
             [ 0,0,0, 0,1,1, 0,1,1], \
             [ 0,0,0,    0, 1, 0,     0,0,0 ], \
             [ 0,0,0 ,0,1,0,1,1, 0] \
             ]

tetrisfield=[]


def rotated(arr):

#1 a 2    3 b 1
#b 5 c    d 5 a
#3 d 4    4 c 2

    new=[0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    
    new[0]=arr[6]
    new[1]=arr[3]
    new[2]=arr[0]

    new[3]=arr[7]
    new[4]=arr[4]
    new[5]=arr[1]
    
    new[6]=arr[8]
    new[7]=arr[5]
    new[8]=arr[2]

    return new


def TetrisDrop( speed ) :
    # drop a tetris block down until it hits something

    # start off the field
    x = -3
    atrow = 2
    atcol = 2
    prevrow = 2
    prevcol = 2

    dropped=False
    colour = random.randint( 0,4) 
    if colour == 0 :
        cr,cg,cb = 255,0,0
    if colour == 1 :
        cr,cg,cb = 0,255,0
    if colour == 2 :
        cr,cg,cb = 0,0,255
    if colour == 3 :
        cr,cg,cb = 128,0,255
    if colour == 3 :
        cr,cg,cb = 255,128,0
    if colour == 4 :
        cr,cg,cb = 0,128,255

    ba=random.randint(0, 9 ) 
    a=tetrisblocks[ba ] 
    print( "Block" )
    print(ba)
    print(a)
    tickct = 0
    tickct = time.ticks_ms()
    while( not dropped ) :
        
            p = 0

            # TODO detect if next draw will hit something if so then exit loop and save new playing field

            # clear last position
            # dont do this unless theres a change of movement to prevent flicker

            if( prevcol != atcol or prevrow != atrow ) :

                for x in range(3):
                    for y in range(3):
                        #if( prevcol + x > 0 and prevrow+y>0) :
                        if( prevcol + x >= 0 and prevrow+y < h and prevrow+y>=0) :
                           picounicorn.set_pixel(prevcol + x , y+prevrow, 0, 0, 0 )

                # draw block moved

                for x in range(3):
                    for y in range(3):
                        if( atcol + x >= 0 and atrow+y < h and atrow+y>=0) :
                            if( a[ p ] == 1 ) : 
                                picounicorn.set_pixel(atcol + x, y+atrow, cr, cg, cb )
                            else:
                                picounicorn.set_pixel(atcol + x, y+atrow, 0, 0, 0 )
                        p = p + 1

            prevrow= atrow
            prevcol = atcol

            # rotate block

            if picounicorn.is_pressed(picounicorn.BUTTON_A): 
                while  picounicorn.is_pressed(picounicorn.BUTTON_A): 
                    pass
                a = rotated(a)





            # TODO detect edge of blocks to allow move right up to sides

            if picounicorn.is_pressed(picounicorn.BUTTON_Y): 
                while  picounicorn.is_pressed(picounicorn.BUTTON_Y): 
                    pass

                # There will always be something in the middle column so just check first and third
                # colummns

                if ( atrow < 5 or ( atrow == 6 and ( a[6] == 0 and a[7] == 0 and a[8] == 0 ) ) ):
                    atrow = atrow + 1


    #            if atrow > 4 :
    #                atrow = 4

            if picounicorn.is_pressed(picounicorn.BUTTON_X): 
                while picounicorn.is_pressed(picounicorn.BUTTON_X): 
                    pass
                if ( atrow > 0 or ( atrow == 0 and ( a[0] == 0 and a[1] == 0 and a[2] == 0 ) ) ):
                    atrow = atrow - 1
                
                #if atrow < 0 :
                #    atrow = 0

            # time to drop a down 

            if time.ticks_diff(time.ticks_ms(), tickct) > speed:
                atcol = atcol + 1
                if atcol == 13 :
                    dropped = True
                tickct = time.ticks_ms()
    
    # TODO save where the current falling block is to the field map


def TetrisPlay() :

    # init the tetris playing field

    rows, cols = (h, w)
    tetrisfield = [[0]*cols]*rows

    
    # setup control display
    clearDisplay()
    CancelButton( "B" )
    LightButton( "X" )
    LightButton( "Y" )
    LightButton( "A" )

    while not picounicorn.is_pressed(picounicorn.BUTTON_B): 
        TetrisDrop( 500 )

        # TODO detect is a line is complete, if so then remove it and drop everything down,
        # redrawing the playing field on display

        # TODO After so many rows are removed, speed the game up
        # TODO if the top row or two has anything in it, the playing field is full up so game over
        # TODO high score is how long the game has run for
        # TODO display highscore table


gameselect = 0

while 1 :
    # display main menu

    #picounicorn.set_pixel(0, 0, 255, 255, 255 )


    #picounicorn.set_pixel(10, 3, 128, 128, 128 )

    #picounicorn.set_pixel(15, 0, 128, 128, 128 )

    OKButton( "A" )
    #CancelButton( "B" )
    LeftButton( "Y" )
    RightButton( "X" )


    # scroll game list
    if picounicorn.is_pressed(picounicorn.BUTTON_Y):  # Left
        while picounicorn.is_pressed(picounicorn.BUTTON_Y): 
            pass
        gameselect = gameselect - 1
        if gameselect < 0 :
            gameselect = 3
        clearDisplay()


    if picounicorn.is_pressed(picounicorn.BUTTON_X):  # Right
        while picounicorn.is_pressed(picounicorn.BUTTON_X): 
            pass
        gameselect = gameselect + 1
        if gameselect > 3 :
            gameselect = 0
        clearDisplay()

    # Display game title page

    if  gameselect == 0 :
        # tetris 
        picounicorn.set_pixel(7, 2, 128, 128, 128 )
        picounicorn.set_pixel(8, 2, 128, 128, 128 )
        picounicorn.set_pixel(9, 2, 128, 128, 128 )
        picounicorn.set_pixel(10,2, 128, 128, 128 )
        picounicorn.set_pixel(7, 3, 128, 128, 128 )
        picounicorn.set_pixel(8, 3, 128, 128, 128 )
        picounicorn.set_pixel(9, 3, 128, 128, 128 )
        picounicorn.set_pixel(10,3, 128, 128, 128 )
        picounicorn.set_pixel(10, 4, 128, 128, 128 )
        picounicorn.set_pixel(9, 4, 128, 128, 128 )
        picounicorn.set_pixel(10, 5, 128, 128, 128 )
        picounicorn.set_pixel(9, 5, 128, 128, 128 )


    if  gameselect == 1 :
        # blitz
        for x in range( 7 ):
            picounicorn.set_pixel(11 - x, 2, 0, 0, 255 )
        for x in range( 3 ):
            picounicorn.set_pixel(11 - x, 3, 0, 0, 255 )
        for x in range( 8 ):
            picounicorn.set_pixel(11 - x, 4, 0, 0, 255 )
        for x in range( 2 ):
            picounicorn.set_pixel(11 - x, 5, 0, 0, 255 )

    # special page displays

    # current battery level

    if gameselect == 2 :
        displayBattery()


    # time to play

    if picounicorn.is_pressed(picounicorn.BUTTON_A):  # Start
        while picounicorn.is_pressed(picounicorn.BUTTON_A): 
            pass
        if gameselect == 0 :
            TetrisPlay()
        clearDisplay()
        NoButton("Y")
        NoButton("X")
        NoButton("B")


# Display a rainbow across Pico Unicorn
#for x in range(w):
#    for y in range(h):
#        r, g, b = [int(c * 255) for c in hsv_to_rgb(x / w, y / h, 1.0)]
#        picounicorn.set_pixel(x, y, r, g, b)
#
#print("Press Button A")
#
#while not picounicorn.is_pressed(picounicorn.BUTTON_A):  # Wait for Button A to be pressed
#    pass
#
## Clear the display
#for x in range(w):
#    for y in range(h):
#        picounicorn.set_pixel(x, y, 0, 0, 0)
#
##print("Button A pressed!")
