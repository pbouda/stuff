# PyQT/OpenGL example
# shaders from here: http://www.iquilezles.org/www/material/nvscene2008/rwwtt.pdf
#
# Author: Peter Bouda, http://www.peterbouda.eu

import time
import array

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
varying vec4 Color;

uniform vec3 LightPosition;
uniform vec3 SurfaceColor;

const float PI = 3.14159;
const float TWO_PI = PI * 2.0;

uniform float Radius;
uniform float Blend;

vec3 sphere(vec2 domain)
{
    vec3 range;
    range.x = Radius * cos(domain.y) * sin(domain.x);
    range.y = Radius * sin(domain.y) * sin(domain.x);
    range.z = Radius * cos(domain.x);
    return range;
}

void main()
{
    vec2 p0 = gl_Vertex.xy * TWO_PI;
    vec3 normal = sphere(p0);;
    vec3 r0 = Radius * normal;
    vec3 vertex = r0;

    normal = mix(gl_Normal, normal, Blend);
    vertex = mix(gl_Vertex.xyz, vertex, Blend);

    normal = normalize(gl_NormalMatrix * normal);
    vec3 position = vec3(gl_ModelViewMatrix * vec4(vertex, 1.0));

    vec3 lightVec = normalize(LightPosition - position);
    float diffuse = max(dot(lightVec, normal), 0.0);

    if (diffuse < 0.125)
         diffuse = 0.125;

    Color = vec4(SurfaceColor * diffuse, 1.0);
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vertex,1.0);
}
'''

    fragmentShaderSource = '''
varying lowp vec4 Color;

void main() {
    gl_FragColor = Color;
}
'''

    def __init__(self, parent=None):
        super(ChocoWindow, self).__init__(parent)
        self.current_blend = 0.0
        self.step_blend = 0.01

    def initialize(self):
        self.program = QtGui.QOpenGLShaderProgram(self)

        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Vertex,
                self.vertexShaderSource)
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Fragment,
                self.fragmentShaderSource)

        self.program.link()
        self.set_uniforms()

    def set_uniforms(self):
        self.program.bind()
        light = QtGui.QVector3D(0.0, 0.0, 5.0);
        self.program.setUniformValue("LightPosition", light);

        surfaceCol = QtGui.QVector3D(0.2, 0.4, 1.0);
        self.program.setUniformValue("SurfaceColor", surfaceCol);

        self.program.setUniformValue("Blend", self.current_blend);
        self.program.setUniformValue("Radius", 0.8);

        # self.matrixUniform = self.program.uniformLocation('matrix')
        # matrix = QtGui.QMatrix4x4()
        # matrix.perspective(60, 4.0/3.0, 0.1, 100.0)
        # matrix.translate(0, 0, -2)
        # self.program.setUniformValue(self.matrixUniform, matrix)

        self.program.release()

    def render(self, gl):
        gl.glViewport(0, 0, self.width(), self.height())
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)


        self.program.bind()

        self.program.setUniformValue("Blend", self.current_blend);

        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3f(0.0, 0.0, 1.0)
        min_v = -0.5
        max_v = 0.5
        range_v = max_v - min_v
        num_x = 64
        num_y = 64
        for on_x in range(num_x):
            for on_y in range(num_y):
                gl.glVertex2f( float(on_x)/float(num_x)*range_v+min_v, float(on_y)/float(num_y)*range_v+min_v)
                gl.glVertex2f( float(on_x+1)/float(num_x)*range_v+min_v, float(on_y)/float(num_y)*range_v+min_v)
                gl.glVertex2f( float(on_x+1)/float(num_x)*range_v+min_v, float(on_y+1)/float(num_y)*range_v+min_v)
                gl.glVertex2f( float(on_x)/float(num_x)*range_v+min_v, float(on_y+1)/float(num_y)*range_v+min_v)

        gl.glEnd()

        self.current_blend += self.step_blend
        if self.current_blend < 0.0:
            self.current_blend = 0.0
            self.step_blend = -self.step_blend
        elif self.current_blend > 1.0:
            self.current_blend = 1.0
            self.step_blend = -self.step_blend

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
