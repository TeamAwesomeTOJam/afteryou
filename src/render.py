import pygame
import game
import numpy
from OpenGL.GL import *
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
        pass
        #vert_shader = createAndCompileShader('''

        #        #version 120
        #        void main() {
        #        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        #        }
        #        ''',GL_VERTEX_SHADER)
        #frag_shader = createAndCompileShader('''
        #        #version 120
        #        void main() {
        #            gl_FragColor = vec4(0,1,0,1);
        #        }
        #        ''',GL_FRAGMENT_SHADER)
        #self.vert_shader =glCreateProgram()
        #glAttachShader(self.vert_shader,vert_shader)
        #glAttachShader(self.vert_shader,frag_shader)
        #glLinkProgram(self.vert_shader)

        #self.vbo = vbo.VBO(
        #        numpy.array([
        #            [ 0, 1, 0],
        #            [-1,-1, 0],
        #            [ 1, 0, 0],
        #            [ 1, 1, 0],
        #            [ 0, 1, 0],
        #            ]),'f')
        #        '''

    def render(self):
        #shaders.glUseProgram(self.vert_shader)

        for view in self.views:
            view.draw()
            
        pygame.display.flip()


class View(object):
    
    def __init__(self, surface, area, layers, entity_name):
        self.surface = surface
        self.area = area
        self.layers = layers
        self.entity_name = entity_name
    
    @property
    def entity(self):
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

