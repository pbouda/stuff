"""
Name		: Water.py
Version		: 1.0
Authors		: Pete "Shredwheat" Shinners and Gareth "Korruptor" Noyce, based on code by Scott Scriven.
Description	: (By G.N.)

    This is a Pygame port of the SDL water effect (http://www.libsdl.org/projects/water/index.html), which is 
    Scot Scriven's port of his old DOS routine (which I started the port from); based on demo code by Federico Feroldi.

    Many thanks to Pete Shinners for guiding me through the Numeric optimisations, fixing the texture mapping
    function and sorting out my mess! It'd never have run fast without his help.

    I've left my direct per-pixel code in the comments in the hope it'll help you work through the Numeric stuff
    that Pete has added. The texturing is serious voodoo though. ;-)

    Note: as this version uses 8bpp it's important that your background images use a sorted palette with a 256
    colour range. You can't just slap any old background in here unfortunately. I've used the same background
    as the original for completness. A quick hack would be for you to draw over it using the same palette and 
    apply the result. ;-) 

Keyboard Controls	:

    "w" 	== "Singing in the rain..."
    "b" 	== "Drop the kids off at the pool" -- repeatedly press b to throw another kid in the pool
    "s" 	== "Everbody gone surfin'"
    "ratbutton" == Quit
    
"""

import pygame, pygame.transform, pygame.image
from operator import *
from random import *
from math import *
from pygame.surfarray import *
from pygame.locals import *
from numpy import *

# ------------------------------------------------------------------------------------
# Glob decs

# Screen resolution...
RES 	= array((1280,720))
CHUNKY  = RES/2
PI 	= 3.14159
DEG2RAD = PI/180

# -----------------------------------------------------------------------------------
def main():
    "Takes the user input, controls the water mode, calls the various height map mods"
    
    # Initialise pygame, and grab an 8bit display.
    pygame.init()
    screen_surface = pygame.display.set_mode(RES,0, 8)

    # Load a source image which we'll use as a background texture for the refraction
    # The palette for this is an ordered 256 colour range for simplicity...
    # The texture buffer is flattened for easier indexing in the texture_map func.
    texture = pygame.image.load("water.gif")

    # Good idea! Fit the texture to the chunky size... 
    texture = pygame.transform.scale(texture, CHUNKY)
    
    
    texture_buff = pygame.surfarray.array2d(texture)
    texture_buff = texture_buff.flat

    # Two blank height maps
    height_buffer = [zeros(CHUNKY, dtype=int),zeros(CHUNKY, dtype=int)]

    # Buffer to draw on...
    water_buffer = zeros(CHUNKY, dtype=int)

    # Texture Lookup Table
    texture_lut = make_indices_array(CHUNKY)


    # Pygame Surface object which will take the surfarray data and be translated into a screen blit... 
    water_surface = pygame.Surface((CHUNKY[0], CHUNKY[1]), 0, 8)
        
    # apply the same palette to surface
    water_surface.set_palette(texture.get_palette())
    screen_surface.set_palette(texture.get_palette())

    # Pointer to the height_buffer we're using...
    hpage = 0

    # Rain drop locators
    x = 80
    y = 80

    # initial surfer angles and placement...
    xang = 0
    yang = 0
    offset = 0
    ox =CHUNKY[0]/2
    oy =CHUNKY[1]/2

    # Water density - change this for jelly or mud effects
    density = 4

    # bobble height
    pheight = 400

    # Strength of the light - increase this for different lighting...
    light = 1

    # Size of blobs
    radius = 15
    
    # Mode 1 = rain (random)
    # Mode 2 = Surfer
    # Mode 3 = Blob
    mode = 0

    # Fruity loops...
    while 1:

        pygame.event.pump()

        # Check for keyboard input...
        keyinput = pygame.key.get_pressed()

        # If ESC or "QUIT" events occurred, exit...
        if keyinput[K_ESCAPE] or pygame.event.peek(QUIT):
            return

        if keyinput[K_w]:
            # Set a raindrop mode...
            mode = 1 

        if keyinput[K_s]:
            # Set the surfer mode...
            mode = 2

        if keyinput[K_b]:
            # Set the blob mode...
            mode = 3

        if mode == 1:
            # Make some noise!
            # pick a random position for our 'drop'
            x = randrange(2,(CHUNKY[0])-2)
            y = randrange(2,(CHUNKY[1])-2)

            # Add it to the height map we're currently working on...
            height_buffer[hpage][x][y] = randrange(1,pheight<<2)

        elif mode == 2:
            # Surfer mode...

            # Calc the new position (could slap this in a table)...
            x = ((CHUNKY[0]/2)-10)*sin((xang*DEG2RAD) * 2)
            y = ((CHUNKY[1]/2)-10)*cos((yang*DEG2RAD) * 3)
            
            xang += 2
            yang += 1

            # Draw a cross in the height map... 
            height_buffer[hpage][int((ox+x))][int((oy+y))] = pheight
            height_buffer[hpage][int((ox+x)+1)][int((oy+y))] = pheight >> 1
            height_buffer[hpage][int((ox+x)-1)][int((oy+y))] = pheight >> 1
            height_buffer[hpage][int((ox+x))][int((oy+y)+1)] = pheight >> 1
            height_buffer[hpage][int((ox+x))][int((oy+y)-1)] = pheight >> 1

        elif mode == 3:
            # Blob mode...
            x = randrange(2,(CHUNKY[0])-2)
            y = randrange(2,(CHUNKY[1])-2)

            # Draw a big blob in the height map
            heightBlob(x,y, pheight, radius, height_buffer[hpage])

            # Reset the mode. Don't dive into the shallow end. 
            mode = 0



        # Draw the water and smooth the map...
        water_buffer = Draw_water(water_buffer, height_buffer[hpage], texture_buff, light-1, texture_lut)
        Calc_water(hpage^1, height_buffer, density)

        # flip to the 'old' height map...
        hpage ^= 1

        # show our audience
        blit_array(water_surface, water_buffer)
        temp = pygame.transform.scale(water_surface, screen_surface.get_size())
        screen_surface.blit(temp, (0,0))
        
        pygame.display.update()


# ------------------------------------------------------------------------------------
def make_indices_array(shape):
    "creates a 3d array where each 2d index is the value"
    a = indices(shape[::-1])
    return transpose(a, (0,2,1))[::-1]
    return a

# ------------------------------------------------------------------------------------
def texturemap(flattened_texture, heightmap, indices_array):
    "tie it all together (all must have same 2d dimensions)"
    shape = heightmap.shape

    distortion = heightmap #>> 1

    indices = array(indices_array)
    indices[0] += distortion
    indices[1] += distortion
    indices[0] %= shape[0]
    indices[1] %= shape[1]

    lookup = indices[0]*shape[1] + indices[1]    
    mapped = take(flattened_texture, lookup.flat)
    return reshape(mapped, shape)

# ------------------------------------------------------------------------------------
def Draw_water(dest, map, texture, LightModifier, indicies):
    "Calcs the heights slopes, applies texturing, returns for screen draw"

    # For each pixel in the buffer, the delta = this_pixel - next_pixel. We don't calculate the edges...
    h_map = zeros(CHUNKY, dtype=int)
    
    thispix = map[1:-1,1:-1] 
    nextpix = map[:-2,1:-1]  
    
    h_map[1:-1,1:-1] = thispix - nextpix
    
    # The array of deltas is then used in the texture mapping to grab source pixels
    # Note: the "python" version of the texture mapping routine is in comments below.
    h_map += texturemap(texture,h_map, indicies) 
    
    # Quick diversion:
    #	for no texturing, comment out the line above, to remove lighting, change the '+=' to '='
            
    
    # Ramp down by our lighting modifier...
    h_map /= int(pow(2, LightModifier))
    
    # Make sure all values are between 0 and 255 (maps to the palette)
    dest = clip(h_map,0,255)
    

    # The slow version... (unless you run this on an SGI you lucky, lucky man...) 
    # --------------------------------------------------------------------------------
    #
    #dx = 0
    #dy = 0
    #x = 0
    #y = 0
    #c = 0
    #
    #for y in range(1, (CHUNKY[1])-1):
    #    for x in range(1,(CHUNKY[0])-1):
    #        # Calculate the slope for the lighting...
    #        dx = map[x][y] - map[x+1][y]
    #        dy = map[x][y] - map[x][y+1]
    #
    #        # Use the slope as offsets and apply texture mapping to the lighting value
    #        c = texture[mod((dx)+x,CHUNKY[0]) + ( mod((dy)+y,CHUNKY[1]) * CHUNKY[1])] - (dx>>LightModifier)
    #        #c = dx>>LightModifier
    #
    #        # Bounds check it...
    #        if (c < 0):
    #            c = 0
    #        elif (c > 255):
    #            c = 255
    #        
    #        # Write this to our surface
    #        dest[x][y] = c
    #
    # --------------------------------------------------------------------------------

    
    # Return the buffer for screen draw...
    return dest

# ------------------------------------------------------------------------------------
def Calc_water(opage, mymap, density):
    "Performs the smothing of the height map..."
    
    # Setup the height maps for reference. 
    new_page = mymap[opage]
    old_page = mymap[opage^1]
    
    center = new_page[1:-1,1:-1]
    origcenter = array(center)
    center[:] = old_page[2:,2:]

    center += old_page[1:-1,2:]
    center += old_page[:-2,2:]
    center += old_page[2:,1:-1]
    center += old_page[:-2,1:-1]
    center += old_page[2:,:-2]
    center += old_page[1:-1,:-2]
    center += old_page[:-2,:-2]

    center /= 4
    center -= origcenter
    center -= (center / int(pow(2, density)))


    # The slow version... 
    # -------------------------------------
    #
    #for y in range(1, (CHUNKY[1])-1):
    #    for x in range(1, (CHUNKY[0])-1):
    #
    #        newh = ((old_page[x-1][y-1] 
    #                + old_page[x][y-1] 
    #                + old_page[x+1][y-1] 
    #                + old_page[x-1][y] 
    #                + old_page[x+1][y] 
    #                + old_page[x-1][y+1] 
    #                + old_page[x][y+1] 
    #                + old_page[x+1][y+1]) >> 2) - new_page[x][y]
    #
    #        new_page[x][y] = newh - (newh >> density)
# ------------------------------------------------------------------------------------

def heightBlob(x, y, height, radius, h_map):
    "Draws a large circle in the height map - Doesn't do the sine effect of the original"

    rquad = 0
    cx = 0
    cy = 0
    cyq = 0
    left = 0
    top = 0
    right = 0
    bottom = 0

    rquad = radius * radius

    # Set the dimensions
    left = -radius
    right = radius
    top = -radius
    bottom = radius

    # Clip it's edges if our placement is going to go south
    if ((x - radius) < 1):
        left -= ((x - radius) - 1)
    if ((y - radius) < 1):
        top -= ((y-radius)-1)
    if ((x + radius) > CHUNKY[0] - 1):
        right -= (x + radius - CHUNKY[0] + 1)
    if ((y + radius) > CHUNKY[1] - 1):
        bottom -= (y + radius - CHUNKY[1] + 1)

    # This draws a large circle in the height map.
    # The original version sloped the height on the edges of the circle
    # to create a "sineblob", but this was a bit slow and didn't look much
    # better than just sticking a large blob in there instead. :-)
    for cy in range (top, bottom):
        cyq = cy*cy
        for cx in range(left, right):
            if(cx*cx + cyq < rquad):
                h_map[cx+x][cy+y] += height

    
# -------------------------------------------------------------------------------
# Brody! We're gonna need a bigger boat!
if __name__ == '__main__': main()

# You wanna see a scar? I've gotta scar...
