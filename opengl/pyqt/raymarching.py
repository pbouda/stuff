# PyQT/OpenGL example
# shaders from here: http://www.iquilezles.org/www/material/nvscene2008/rwwtt.pdf
#
# Author: Peter Bouda, http://www.peterbouda.eu

import time
import array
import math

from PyQt5.QtMultimedia import *
from PyQt5 import QtCore, QtGui, QtWidgets


class OpenGLWindow(QtGui.QWindow):
    def __init__(self, parent=None):
        super(OpenGLWindow, self).__init__(parent)

        self.m_update_pending = False
        self.m_animating = False
        self.m_context = None
        self.m_gl = None

        self.setSurfaceType(QtGui.QWindow.OpenGLSurface)

    def initialize(self):
        pass

    def setAnimating(self, animating):
        self.m_animating = animating

        if animating:
            self.renderLater()

    def renderLater(self):
        if not self.m_update_pending:
            self.m_update_pending = True
            QtGui.QGuiApplication.postEvent(self, QtCore.QEvent(QtCore.QEvent.UpdateRequest))

    def renderNow(self):
        if not self.isExposed():
            return

        self.m_update_pending = False

        needsInitialize = False

        if self.m_context is None:
            self.m_context = QtGui.QOpenGLContext(self)
            self.m_context.setFormat(self.requestedFormat())
            self.m_context.create()

            needsInitialize = True

        self.m_context.makeCurrent(self)

        if needsInitialize:
            version = QtGui.QOpenGLVersionProfile()
            version.setVersion(2, 0)
            self.m_gl = self.m_context.versionFunctions(version)
            self.m_gl.initializeOpenGLFunctions()

            self.initialize()

        self.render(self.m_gl)

        self.m_context.swapBuffers(self)

        if self.m_animating:
            self.renderLater()

    def event(self, event):
        if event.type() == QtCore.QEvent.UpdateRequest:
            self.renderNow()
            return True

        return super(OpenGLWindow, self).event(event)

    def exposeEvent(self, event):
        self.renderNow()

    def resizeEvent(self, event):
        self.renderNow()


class ChocoWindow(OpenGLWindow):
    
    vertexShaderSource = '''
attribute highp vec4 vPosition;
uniform highp vec4 cam;
uniform highp vec4 origin;
uniform highp vec4 ray;
varying highp vec4 tc[2];

void main(void)
{
    gl_Position=vPosition;
    vec3 d=normalize(origin.xyz-cam.xyz);
    vec3 r=normalize(cross(d,vec3(0.0,1.0,0.0)));
    vec3 u=cross(r,d);
    vec3 e=vec3(vPosition.x*1.333,vPosition.y,.75);   //    eye space ray
    tc[0].xyz=mat3(r,u,d)*e;                 //  world space ray
    tc[1]=vec4(.5)+vPosition*.5;             // screen space coordinate
}
'''

    fragmentShaderSource = '''
uniform highp vec4 cam;
uniform highp vec4 origin;
uniform highp vec4 ray;
varying highp vec4 tc[2];

highp float interesctSphere(in highp vec3 rO, in highp vec3 rD, in highp vec4 sph)
{
    highp vec3 p = rO - sph.xyz;
    highp float b = dot( p, rD );
    highp float c = dot( p, p ) - sph.w*sph.w;
    highp float h = b*b - c;
    if( h>0.0 )
    {
        h = -b - sqrt( h );
    }
    return h;
}

void main(void)
{
    highp vec3 wrd = normalize(tc[0].xyz);
    highp vec3 wro = cam.xyz;
    highp float dif = dot( origin.xy-vec2(0.5), vec2(0.707) );

    highp float t = interesctSphere(wro,wrd,ray);
    if(t>0.0)
    {
        highp vec3 inter = wro + t*wrd;
        highp vec3 norma = normalize( inter - ray.xyz );
        dif = dot(norma,vec3(0.57703));
    }
    gl_FragColor = dif*vec4(0.5,0.4,0.3,0.0) + vec4(0.5,0.5,0.5,1.0);
}
'''

    def __init__(self, parent=None):
        super(ChocoWindow, self).__init__(parent)
        self.current_blend = 0.0
        self.step_blend = 0.01
        self.start_time = time.clock()

    def initialize(self):
        self.program = QtGui.QOpenGLShaderProgram(self)

        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Vertex,
                self.vertexShaderSource)
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Fragment,
                self.fragmentShaderSource)

        self.program.link()

        self.vAttr = self.program.attributeLocation('vPosition')

    def render(self, gl):
        gl.glViewport(0, 0, self.width(), self.height())
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        self.program.bind()

        t = time.clock() - self.start_time

        cam = QtGui.QVector4D(2.0*math.sin(1.0*t + 0.1),  0.0, 2.0*math.cos(1.0*t), 0.0)
        self.program.setUniformValue("cam", cam);
        origin = QtGui.QVector4D(0.0, 0.0, 0.0, 0.0)
        self.program.setUniformValue("origin", origin)
        ray = QtGui.QVector4D(0.0, 0.0, 0.0, 1.0)
        self.program.setUniformValue("ray", ray)

        vertices = array.array("f", [
             1,  1, 0,
            -1,  1, 0,
            -1, -1, 0,
             1, -1, 0
        ])

        indices = array.array("B", [0,1,2,0,2,3])

        gl.glEnableVertexAttribArray(self.vAttr)

        gl.glVertexAttribPointer(self.vAttr,
            3,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            0,
            vertices)

        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_BYTE, indices)

        gl.glDisableVertexAttribArray(self.vAttr)

        self.program.release()


if __name__ == '__main__':
    import sys
 
    app = QtWidgets.QApplication(sys.argv)
    
    format = QtGui.QSurfaceFormat()
    format.setSamples(4)

    window = ChocoWindow()
    window.setFormat(format)
    window.resize(640, 480)
    window.show()

    window.setAnimating(True)

    sys.exit(app.exec_())
