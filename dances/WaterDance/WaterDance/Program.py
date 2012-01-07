 # ############################################################################
 #
 # Copyright (c) Microsoft Corporation. 
 #
 # Available under the Microsoft PyKinect 1.0 Alpha license.  See LICENSE.txt
 # for more information.
 #
 # ###########################################################################/

import thread
import itertools
import ctypes

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

import numpy
from operator import *
from random import *
from math import *

KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 640,480
pygame.init()

# Screen resolution...
RES 	= numpy.array((DEPTH_WINSIZE))
CHUNKY  = RES/2
PI 	= 3.14159
DEG2RAD = PI/180

# recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes


def depth_frame_ready(frame):
    global depth_frame_bits
    if video_display:
        return

    #depth_frame_array = numpy.ctypeslib.as_array(frame.image.bits)

    depth_frame_bits = frame.image.bits

    #address = surface_to_array(dept_frame_surface)
    #ctypes.memmove(address, frame.image.bits, len(address))
    #del address
    #pygame.display.update()    

# ------------------------------------------------------------------------------------
def make_indices_array(shape):
    "creates a 3d array where each 2d index is the value"
    a = numpy.indices(shape[::-1])
    return numpy.transpose(a, (0,2,1))[::-1]

# ------------------------------------------------------------------------------------
def texturemap(flattened_texture, heightmap, indices_array):
    "tie it all together (all must have same 2d dimensions)"
    shape = heightmap.shape

    distortion = heightmap #>> 1

    indices = numpy.array(indices_array)
    indices[0] += distortion
    indices[1] += distortion
    indices[0] %= shape[0]
    indices[1] %= shape[1]

    lookup = indices[0]*shape[1] + indices[1]    
    mapped = numpy.take(flattened_texture, lookup.flat)
    return numpy.reshape(mapped, shape)

# ------------------------------------------------------------------------------------
def Draw_water(dest, map, texture, LightModifier, indicies):
    "Calcs the heights slopes, applies texturing, returns for screen draw"

    # For each pixel in the buffer, the delta = this_pixel - next_pixel. We don't calculate the edges...
    h_map = numpy.zeros(CHUNKY, dtype=int)
    
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
    dest = numpy.clip(h_map,0,255)
    
    # Return the buffer for screen draw...
    return dest

# ------------------------------------------------------------------------------------
def Calc_water(opage, mymap, density):
    "Performs the smothing of the height map..."
    
    # Setup the height maps for reference. 
    new_page = mymap[opage]
    old_page = mymap[opage^1]
    
    center = new_page[1:-1,1:-1]
    origcenter = numpy.array(center)
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


if __name__ == '__main__':
    full_screen = True
    draw_skeleton = False
    video_display = False

    depth_frame_bits = None

    display_flags = 0
    if full_screen:
        display_flags = pygame.FULLSCREEN

    screen_lock = thread.allocate()

    screen = pygame.display.set_mode(DEPTH_WINSIZE, display_flags, 16)    
    pygame.display.set_caption('Python Kinect Demo')
    skeletons = None
    screen.fill(THECOLORS["black"])

    kinect = nui.Runtime()

    kinect.depth_frame_ready += depth_frame_ready    
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)

    print('Controls: ')
    print('     d - Switch to depth view')
    print('     v - Switch to video view')
    print('     s - Toggle displaing of the skeleton')
    print('     u - Increase elevation angle')
    print('     j - Decrease elevation angle')

    # main game loop
    done = False

    texture = pygame.image.load("water.gif")

    # Good idea! Fit the texture to the chunky size... 
    texture = pygame.transform.scale(texture, CHUNKY)
    
    texture_buff = pygame.surfarray.array2d(texture)
    texture_buff = texture_buff.flat

    # Two blank height maps
    height_buffer = [numpy.zeros(CHUNKY, dtype=int), numpy.zeros(CHUNKY, dtype=int)]

    # Buffer to draw on...
    water_buffer = numpy.zeros(CHUNKY, dtype=int)

    # Texture Lookup Table
    texture_lut = make_indices_array(CHUNKY)


    # Pygame Surface object which will take the surfarray data and be translated into a screen blit... 
    water_surface = pygame.Surface((CHUNKY[0], CHUNKY[1]), 0, 8)
    depth_surface = pygame.Surface(RES, 0, 8)
    #screen_surface = pygame.Surface(RES, 0, 16)
        
    # apply the same palette to surface
    water_surface.set_palette(texture.get_palette())
    grayscale = tuple([(i, i, i) for i in range(255, -1, -1)])
    depth_surface.set_palette(grayscale)
    #screen_surface.set_palette(texture.get_palette())

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

    while not done:
#        e = pygame.event.wait()
#        dispInfo = pygame.display.Info()
        pygame.event.pump()

        # Check for keyboard input...
        keyinput = pygame.key.get_pressed()

        # If ESC or "QUIT" events occurred, exit...
        if keyinput[K_ESCAPE] or pygame.event.peek(QUIT):
            done = True
            break
        elif keyinput[K_u]:
            kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
        elif keyinput[K_j]:
            kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
        elif keyinput[K_x]:
            kinect.camera.elevation_angle = 2

        elif keyinput[K_w]:
            mode = 1 
        elif keyinput[K_s]:
            mode = 2
        elif keyinput[K_b]:
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

        pygame.surfarray.blit_array(water_surface, water_buffer)
        temp = pygame.transform.scale(water_surface, screen.get_size())
        temp = temp.convert(16)

        if depth_frame_bits:
            data = numpy.fromstring(depth_frame_bits, dtype=numpy.uint16)
            data &= 8191
            data.resize((480, 640))
            data -= numpy.min(data.ravel())
            data *= float(256) / float(numpy.max(data.ravel()))
            pygame.surfarray.blit_array(depth_surface, data.transpose())

        screen.blit(temp, (0,0))
        #screen.blit(depth_surface, (0,0))
        screen.blit(depth_surface, (0,0), None, pygame.BLEND_SUB)
                
        pygame.display.update()
