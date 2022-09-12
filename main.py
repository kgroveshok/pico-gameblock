import picounicorn
from machine import ADC, Pin

import time
import random

picounicorn.init()








# Main loop

w = picounicorn.get_width()
h = picounicorn.get_height()

def clearDisplay():

    for x in range(w):
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


def TetrisPlay() :


    # block defs

    blocks = [  \
             [ 0, 0, 1, 0, 0, 1, 0, 1, 1 ], \
             [ 1, 1, 1, 1, 1, 0, 1, 0, 0 ], \
             [ 1, 1, 0, 1, 0, 0, 1, 1, 0 ], \
             [ 1, 1, 1, 1, 0, 0, 1, 1, 1 ], \
             [ 0, 0, 1, 0, 1, 1, 0, 0, 1 ], \
             [ 0,0,1,0,0,1, 0,0,1], \
             [ 1,0,0, 1,0,0, 1,1,0], \
             [ 0,0,0, 0,1,1, 0,1,1], \
             [ 0,0,0,    0, 0, 0,     0,0,1 ], \
             [ 0,0,0,      0,0,1,        0,0,1], \
             [    0,0,0,      0,0,1,                0,1,1 ] \
             ]


    
    # setup control display
    clearDisplay()
    CancelButton( "B" )
    LightButton( "X" )
    LightButton( "Y" )
    LightButton( "A" )

    while not picounicorn.is_pressed(picounicorn.BUTTON_B): 

        for a in blocks :
            p = 0
            colour = random.randint( 0,3 ) 
            cr = 0
            cg = 0
            cb = 255
            if colour == 0 :
                cr = 255
            if colour == 1 :
                cg = 255

            for x in range(3):
                for y in range(3):
                    if( a[ p ] == 1 ) : 
                        picounicorn.set_pixel(5+x, y+2, cr, cg, cb )
                    else:
                        picounicorn.set_pixel(5+x, y+2, 0, 0, 0 )
                    p = p + 1
            time.sleep(0.5)


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
