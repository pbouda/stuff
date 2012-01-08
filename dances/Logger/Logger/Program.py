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
import time

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 640,480
VIDEO_WINSIZE = 640,480
pygame.init()

LOG = open("data.log", "w")

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter,
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
LEFT_ARM_NAMES = ("JointId.ShoulderCenter",
            "JointId.ShoulderLeft", 
            "JointId.ElbowLeft", 
            "JointId.WristLeft", 
            "JointId.HandLeft")

RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
RIGHT_ARM_NAMES = ("JointId.ShoulderCenter", 
             "JointId.ShoulderRight", 
             "JointId.ElbowRight", 
             "JointId.WristRight", 
             "JointId.HandRight")

LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
LEFT_LEG_NAMES = ("JointId.HipCenter", 
            "JointId.HipLeft", 
            "JointId.KneeLeft", 
            "JointId.AnkleLeft", 
            "JointId.FootLeft")

RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
RIGHT_LEG_NAMES = ("JointId.HipCenter", 
             "JointId.HipRight", 
             "JointId.KneeRight", 
             "JointId.AnkleRight", 
             "JointId.FootRight")

SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)
SPINE_NAMES = ("JointId.HipCenter", 
         "JointId.Spine", 
         "JointId.ShoulderCenter", 
         "JointId.Head")

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

frame_nr = 0

def draw_skeleton_data(pSkelton, index, positions, names, ts, idskel, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
    print >>LOG, "%s,%s,%s,%s" % (ts, idskel, names[0], start)

    i = 1
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next
        print >>LOG, "%s,%s,%s,%s" % (ts, idskel, names[i], start)
        i += 1

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

def draw_skeletons(skeletons):
    global frame_nr
    for index, data in enumerate(skeletons):
        if (data.eTrackingState == nui.SkeletonTrackingState.TRACKED):
            # draw the Head
            #timestamp = time.time()
            timestamp = frame_nr
            #print >>LOG, index
            #print >>LOG, data
            HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
            #print >>LOG, "%s,%s,JointId.Head,%s" % (timestamp,index,data.SkeletonPositions[JointId.Head])
            draw_skeleton_data(data, index, SPINE, SPINE_NAMES, timestamp, index, 10)
            pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
    
            # drawing the limbs
            draw_skeleton_data(data, index, LEFT_ARM, LEFT_ARM_NAMES, timestamp, index)
            draw_skeleton_data(data, index, RIGHT_ARM, RIGHT_ARM_NAMES, timestamp, index)
            draw_skeleton_data(data, index, LEFT_LEG, LEFT_LEG_NAMES, timestamp, index)
            draw_skeleton_data(data, index, RIGHT_LEG, RIGHT_LEG_NAMES, timestamp, index)

        frame_nr += 1

def depth_frame_ready(frame):
    if video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        frame_bits = frame.image.bits
        print frame_bits
        ctypes.memmove(address, frame.image.bits, len(address))
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()


if __name__ == '__main__':
    full_screen = True
    draw_skeleton = True
    video_display = False

    display_flags = 0
    if full_screen:
        display_flags = pygame.FULLSCREEN

    screen_lock = thread.allocate()

    screen = pygame.display.set_mode(DEPTH_WINSIZE, display_flags, 16)    
    pygame.display.set_caption('Python Kinect Demo')
    skeletons = None
    screen.fill(THECOLORS["black"])

    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True
    def post_frame(frame):
        try:
            pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
            # event queue full
            pass

    kinect.skeleton_frame_ready += post_frame
    
    kinect.depth_frame_ready += depth_frame_ready    
    #kinect.video_frame_ready += video_frame_ready    
    
    #kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)

    print('Controls: ')
    print('     s - Toggle displaing of the skeleton')
    print('     u - Increase elevation angle')
    print('     j - Decrease elevation angle')

    # main game loop
    done = False

    while not done:
        e = pygame.event.wait()
        dispInfo = pygame.display.Info()
        if e.type == pygame.QUIT:
            done = True
            LOG.close()
            break
        elif e.type == KINECTEVENT:
            skeletons = e.skeletons
            if draw_skeleton:
                draw_skeletons(skeletons)
                pygame.display.update()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                done = True
                break
            elif e.key == K_s:
                draw_skeleton = not draw_skeleton
            elif e.key == K_u:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
            elif e.key == K_j:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
            elif e.key == K_x:
                kinect.camera.elevation_angle = 2
