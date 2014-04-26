import pygame
import game
import math
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
#from OpenGLContext.arrays import *


def createAndCompileShader(source,type):
    shader=glCreateShader(type)
    glShaderSource(shader,source)
    glCompileShader(shader)

    # get "compile status" - glCompileShader will not fail with 
    # an exception in case of syntax errors
    result=glGetShaderiv(shader,GL_COMPILE_STATUS)

    if (result!=1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
    return shader

class Render(object):
    def __init__(self):
        glutInit()
        vert_shader = createAndCompileShader('''

                #version 120
                void main() {
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                }
                ''',GL_VERTEX_SHADER)
        frag_shader = createAndCompileShader('''
                #version 120
                void main() {
                    gl_FragColor = vec4(0,1,0,1);
                }
                ''',GL_FRAGMENT_SHADER)
        self.vert_shader =glCreateProgram()
        glAttachShader(self.vert_shader,vert_shader)
        glAttachShader(self.vert_shader,frag_shader)
        glLinkProgram(self.vert_shader)

        self.vbo = vbo.VBO(
                numpy.array([
                    [ 0, 1, 0],
                    [-1,-1, 0],
                    [ 1, 0, 0],
                    [ 1, 1, 0],
                    [ 0, 1, 0],
                    ]))

        self.p1 = (0,0)
        self.p2 = (.1,.1)
    def set_p1(self,x, y):
        self.p1 = (int(float(x)/self.x),int(float(y)/self.y))
    def set_p2(self,x, y):
        self.p2 = (int(float(x)/self.x),int(float(y)/self.y))
        

    def resize(self,tup):
        x,y = tup
        self.x = x
        self.y = y
        gluOrtho2D(-1,1,-1,1)
    
    def drawCircle(self,x,y):
        x = float(x) / self.x -.5
        y = float(y) / self.y -.5
        print x,y
        glBegin(GL_TRIANGLE_FAN)
        num_div = 30
        dx = 2.0/(num_div-1) * math.pi
        for i in xrange(num_div):
            glVertex2f(x+math.cos(dx * i) * .1, y + math.sin(dx * i) *.1)
        glEnd()




    def render(self):
        print "Render!"
        glUseProgram(self.vert_shader)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        #glutSolidTeapot(1.0)

        #for view in self.views:
        #    view.draw()
        glColor3f(1,1,1);
        glBegin(GL_LINES)
        glVertex2f(self.p1[0],self.p1[1])
        glVertex2f(self.p2[0],self.p2[1])
        glEnd()

        em = game.get_game().entity_manager


        p1 = em.get_by_name('player1')
        p1col = p1.color
        glColor3i(p1col[0],p1col[1],p1col[2])
        self.drawCircle(p1.x,p1.y)

        p2 = em.get_by_name('player2')
        p2col = p2.color
        glColor3i(p2col[0],p2col[2],p2col[2])
        glColor3f(1,1,1)
        self.drawCircle(p2.x,p2.y)


        try:
            self.vbo.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointerf(self.vbo)
                glDrawArrays(GL_TRIANGLES,0,5)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)
        finally:
            glUseProgram(0)
            
        pygame.display.flip()


class View(object):
    
    def __init__(self, surface, area, layers=None, entity_name=None):
        self.surface = surface
        self.area = area
        self.layers = layers if layers != None else []
        self.entity_name = entity_name
    
    @property
    def entity(self):
        if self.entity_name:
            return game.get_game().entity_manager.get_by_name(self.entity_name)
    
    def add_layer(self, layer):
        self.layers.append(layer)
        
    def draw(self):
        self.surface.set_clip(self.area)
        
        for layer in self.layers:
            layer.draw(self)
            
        self.surface.set_clip(None)


class StaticLayer(object):
    
    def __init__(self, size, tag):
        self.size = size
        self.tag = tag
        self.surface = pygame.Surface(self.size)
        self.surface.convert()
        
        transform = lambda x, y : (x, y)
        
        for entity in game.get_game().entity_manager.get_by_tag(tag):
            entity.handle('draw', self.surface, transform)
        
    def draw(self, view):
        area_to_blit = pygame.Rect(view.area)
        area_to_blit.center = (view.entity.x, view.entity.y)
        view.surface.blit(self.surface, view.area, area_to_blit)
    

class DepthSortedLayer(object):
    
    def __init__(self, tag):
        self.tag = tag
        
    def draw(self, view):
        area_to_blit = pygame.Rect(view.area)
        area_to_blit.center = (view.entity.x, view.entity.y)   

        entities_to_draw = sorted(game.get_game().entity_manager.get_in_area(self.tag, area_to_blit, precise=False), key=lambda entity: entity.y)

        transform = lambda x, y : (x - area_to_blit.x + view.area.x, y - area_to_blit.y + view.area.y)
        
        for entity in entities_to_draw:
            entity.handle('draw', view.surface, transform)


class BackgroundLayer(object):
    
    def draw(self, view):
        r = pygame.Rect(view.area)
        p = 1
        for x in range(0, view.area.width, 100):
            r.left = x
            pygame.draw.rect(view.surface, game.get_game().entity_manager.get_by_name('player' + str(1+p)).color, r)
            p = (p + 1) % 2
            

class SimpleLayer(object):
    
    def __init__(self, tag):
        self.tag = tag
        
    def draw(self, view):        
        for entity in game.get_game().entity_manager.get_by_tag(self.tag):
            entity.handle('draw', view.surface, lambda x, y : (x, y))
