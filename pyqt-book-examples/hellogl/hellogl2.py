# -*- coding: utf-8 -*-

import sys, numpy
from PyQt4 import QtCore, QtGui, QtOpenGL
import OpenGL.GL
import OpenGL.GLU

from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, \
        glCreateProgram, glGetUniformLocation, glUniform1i, \
        glUniform1f, glLinkProgram, glCreateShader, glUseProgram, \
        glAttachShader, glCompileShader, glShaderSource, \
        glGetProgramInfoLog, glGetShaderInfoLog

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


class ShaderException(Exception):
    '''Exception launched by shader in error case'''
    pass
  
class Shader(object):
    '''Create a vertex or fragment shader
  
    :Parameters:
        `vertex_source` : string, default to None
            Source code for vertex shader
        `fragment_source` : string, default to None
            Source code for fragment shader
    '''
    def __init__(self, vertex_source=None, fragment_source=None):
        self.program = glCreateProgram()
  
        if vertex_source:
            self.vertex_shader = self.create_shader(
                vertex_source, GL_VERTEX_SHADER)
            glAttachShader(self.program, self.vertex_shader)
  
        if fragment_source:
            self.fragment_shader = self.create_shader(
                fragment_source, GL_FRAGMENT_SHADER)
            glAttachShader(self.program, self.fragment_shader)
  
        glLinkProgram(self.program)
        message = self.get_program_log(self.program)
        if message:
            pymt_logger.debug('Shader: shader program message: %s' % message)
  
    def create_shader(self, source, shadertype):
        shader = glCreateShader(shadertype)
        # PyOpenGL bug ? He's waiting for a list of string, not a string
        # on some card, it failed :)
        if isinstance(source, basestring):
            source = [source]
        glShaderSource(shader, source)
        glCompileShader(shader)
        message = self.get_shader_log(shader)
        if message:
            pymt_logger.debug('Shader: shader message: %s' % message)
        return shader
  
    def set_uniform_f(self, name, value):
        location = glGetUniformLocation(self.program, name)
        glUniform1f(location, value)
  
    def set_uniform_i(self, name, value):
        location = glGetUniformLocation(self.program, name)
        glUniform1i(location, value)
  
    def __setitem__(self, name, value):
        """pass a variable to the shader"""
        if isinstance(value, float):
            self.set_uniform_f(name, value)
        elif isinstance(value, int):
            self.set_uniform_i(name, value)
        else:
            raise TypeError('Only single floats and ints are supported so far')
  
    def use(self):
        '''Use the shader'''
        glUseProgram(self.program)
  
    def stop(self):
        '''Stop using the shader'''
        glUseProgram(0)
  
    def get_shader_log(self, shader):
        '''Return the shader log'''
        return self.get_log(shader, glGetShaderInfoLog)
  
    def get_program_log(self, shader):
        '''Return the program log'''
        return self.get_log(shader, glGetProgramInfoLog)
  
    def get_log(self, obj, func):
        value = func(obj)
        return value


class MainWindow(QtOpenGL.QGLWidget):

    def __init__(self, *args):
        QtOpenGL.QGLWidget.__init__(self, *args)
        self.identityshader = Shader('''
            attribute vec4 vVertex;
            void main(void) {
                gl_Position = vVertex;
            }
            ''', '''
            uniform vec4 vColor;
            void main(void) {
                gl_FragColor = vColor;
            }
            ''')

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)
        
    def sizeHint(self):
        return QtCore.QSize(400, 400)
        
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))

    def paintGL(self):
        self.identityshader.use()
        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
        OpenGL.GL.glLoadIdentity()
        #vRed = [ 1.0, 0.0, 0.0, 1.0 ]
        #self.identityshader["vColor"] = vRed
        OpenGL.GL.glColor3fv((25, 123, 180))
        OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLES)
        OpenGL.GL.glVertex3f( 0.0, 0.5, 0.0) 
        OpenGL.GL.glVertex3f(-0.5,-0.5, 0.0)
        OpenGL.GL.glVertex3f( 0.5,-0.5, 0.0)
        OpenGL.GL.glEnd()
        self.identityshader.stop()
        
    def resizeGL(self, w, h):
        OpenGL.GL.glViewport(0, 0, w, h);

if __name__ == "__main__":
    main(sys.argv)