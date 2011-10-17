# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
import cv

camera_index = 0
min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class FaceDetect:
    
    def __init__(self):
        self.cascade = cv.Load("haarcascade_frontalface_alt.xml")
        self.captureStarted = False
        self.frame_copy = None
    
    def startCapture(self):
        self.capture = cv.CreateCameraCapture(camera_index)
        self.captureStarted = True

    def stopCapture(self):
        self.captureStarted = False
    
    def frame(self):
        if self.captureStarted:
            frame = cv.QueryFrame(self.capture)
                
            if not self.frame_copy:
                self.frame_copy = cv.CreateImage((frame.width,frame.height),
                                                 cv.IPL_DEPTH_8U, frame.nChannels)

            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, self.frame_copy)
            else:
                cv.Flip(frame, self.frame_copy, 0)
                
            self.detectFaces()
            

        return self.frame_copy
        
    def detectFaces(self):
        # allocate temporary images
        gray = cv.CreateImage((self.frame_copy.width, self.frame_copy.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(self.frame_copy.width / image_scale),
                                    cv.Round(self.frame_copy.height / image_scale)), 8, 1)
    
        # convert color input image to grayscale
        cv.CvtColor(self.frame_copy, gray, cv.CV_BGR2GRAY)
    
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
    
        cv.EqualizeHist(small_img, small_img)
        

        if(self.cascade):
            t = cv.GetTickCount()
            faces = cv.HaarDetectObjects(small_img, self.cascade, cv.CreateMemStorage(0),
                                         haar_scale, min_neighbors, haar_flags, min_size)
            t = cv.GetTickCount() - t
            print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
            if faces:
                for ((x, y, w, h), n) in faces:
                    # the input to cv.HaarDetectObjects was resized, so scale the 
                    # bounding box of each face and convert it to two CvPoints
                    pt1 = (int(x * image_scale), int(y * image_scale))
                    pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                    cv.Rectangle(self.frame_copy, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)


class MainWindow(QtOpenGL.QGLWidget):

    def __init__(self, *args):
        QtOpenGL.QGLWidget.__init__(self, *args)
        
        self.detector = FaceDetect()        
        self.detector.startCapture()
        
        self.frame = None
        self.angle = 0.0

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateWorld)
        self.timer.start(100)

    def updateWorld(self):
        self.frame = self.detector.frame()
        self.angle = self.angle + 5.0
        self.updateGL()
        
    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)        
        glClearDepth(1.0)
        glMatrixMode(GL_PROJECTION)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        if self.frame != None:
            glDrawPixels(self.width(), self.height(), GL_RGB, GL_UNSIGNED_BYTE, self.frame.tostring()[::-1])

        glRotatef(self.angle, 0.0, 1.0, 0.0)

        glColor(0.1, 0.5, 0.8)
        glBegin(OpenGL.GL.GL_TRIANGLES)
        glVertex3f( 0.0, 0.5, 0.0) 
        glVertex3f(-0.5,-0.5, 0.0)
        glVertex3f( 0.5,-0.5, 0.0)
        glEnd()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height);
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

if __name__ == "__main__":
    main(sys.argv)