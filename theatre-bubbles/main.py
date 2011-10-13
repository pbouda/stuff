#!/usr/bin/env python

import sys, os, traceback
from PyQt4 import QtCore, QtGui, QtDeclarative
import cv

camera_index = 0
min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0


class FaceDetect:    
    def __init__(self):
        self.cascade = cv.Load("haarcascades/haarcascade_frontalface_alt.xml")
        self.capture_started = False
        self.frame_copy = None
    
    def start_capture(self):
        self.capture = cv.CreateCameraCapture(camera_index)
        self.capture_started = True

    def stop_capture(self):
        self.capture_started = False
        
    def frame_size(self):
        if self.frame_copy:
            return(self.frame_copy.width, self.frame_copy.height)
        else:
            return(0, 0)
            
    def frame(self):
        if self.capture_started:
            frame = cv.QueryFrame(self.capture)
                
            if not self.frame_copy:
                self.frame_copy = cv.CreateImage((frame.width,frame.height),
                                                 cv.IPL_DEPTH_8U, frame.nChannels)

            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, self.frame_copy)
            else:
                cv.Flip(frame, self.frame_copy, 0)
                
 
    def detect_faces(self):
        self.frame()
        
        # allocate temporary images
        gray = cv.CreateImage((self.frame_copy.width, self.frame_copy.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(self.frame_copy.width / image_scale),
                                    cv.Round(self.frame_copy.height / image_scale)), 8, 1)
    
        # convert color input image to grayscale
        cv.CvtColor(self.frame_copy, gray, cv.CV_BGR2GRAY)
    
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
    
        cv.EqualizeHist(small_img, small_img)
        
        faces = cv.HaarDetectObjects(small_img, self.cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)

        return faces


class MainWindow(QtDeclarative.QDeclarativeView):
    
    def __init__(self, *args):
        QtDeclarative.QDeclarativeView.__init__(self, *args)
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

        self.faces = [ [0,0] ]

        context = self.rootContext()
        context.setContextProperty("modelFaces", self.faces)

        self.setSource(QtCore.QUrl("qml/main2.qml"))
            
        self.detector = FaceDetect()        
        self.detector.start_capture()        

        self.detector.frame()
        self.frame_width, self.frame_height = self.detector.frame_size()
        self.frame_width = float(self.frame_width) / image_scale
        self.frame_height = float(self.frame_height) / image_scale

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateCoords)
        self.timer.start(100)        

    def updateCoords(self):
        f = self.detector.detect_faces()
        if len(f) > 0:
            self.faces = []
            
            for coords, n in f:
                x = self.width() - int((float(coords[0]) / self.frame_width) * self.width())
                y = int((float(coords[1]) / self.frame_height) * self.height())
                
                #print coords[0]
                #print self.frame_width
                #print x
                #print self.width()
                #print
                #print coords[1]
                #print self.frame_height
                #print y
                #print self.height()
                #print
                
                self.faces.append([x, y])
                
            context = self.rootContext()
            context.setContextProperty("modelFaces", self.faces)
        
def main(argv):
    app = QtGui.QApplication(argv)
    view = MainWindow()
    
    #glw = QtOpenGL.QGLWidget()
    #view.setViewport(glw)
    #view.showFullScreen()
    
    view.resize(800, 600)
    view.show()

    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
