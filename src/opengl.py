import pygame
import game
import math
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GL.framebufferobjects import *

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

class FrameBufferObject:
    def __init__(self, width = 256, height = 256):
        # Save dimensions
        self.width, self.height = width, height
        
        # Generate a framebuffer ID
        self.id = glGenFramebuffers(1)
        
        # The texture we're going to render to
        self.gl_tex_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.gl_tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)

        glBindFramebuffer(GL_FRAMEBUFFER, self.id)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.gl_tex_id, 0)
        
        glDrawBuffers([GL_COLOR_ATTACHMENT0])

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print "Framebuffer incomplete: %s" % glCheckFramebufferStatus(GL_FRAMEBUFFER)
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_ALPHA_TEST)
        self.clear()
    
    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.id)
        glPushAttrib(GL_VIEWPORT_BIT) # save viewport
        glViewport(0, 0, self.width, self.height)
    
    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glPopAttrib()
    
    def clear(self):
        self.bind()
        glClearColor(0.0, 0.0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.unbind()



class GLRenderer:
    def __init__(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA);
        self.circle_queue = []
        self.rectangle_queue = []
        self.draw_queue = []
        vert_shader = createAndCompileShader('''

                #version 120
                uniform float aspectRatio;
                void main() {
                    vec4 v = gl_Vertex;
                    v.y = v.y * aspectRatio;
                gl_Position = gl_ModelViewProjectionMatrix * v;
                }
                ''',GL_VERTEX_SHADER)
        frag_shader = createAndCompileShader('''
                #version 120
                uniform vec3 color;
                void main() {
                    gl_FragColor = vec4(color,1.0);
                }
                ''',GL_FRAGMENT_SHADER)
        self.player_shader =glCreateProgram()
        glAttachShader(self.player_shader,vert_shader)
        glAttachShader(self.player_shader,frag_shader)
        glLinkProgram(self.player_shader)


        gluOrtho2D(0,1,0,1)

        self.vbo = vbo.VBO(
                numpy.array([
                    [ 0, 1, 0],
                    [-1,-1, 0],
                    [ 1, 0, 0],
                    [ 1, 1, 0],
                    [ 0, 1, 0],
                    ]))
        fbox = 1280
        fboy = 720
        self.fbo = FrameBufferObject(fbox,fboy)
        self.bg_fbo = FrameBufferObject(fbox,fboy)
        self.finalRenderShader();
        self.resize((fbox,fboy))
        self.cleanup()

    
    def finalRenderShader(self):
        vert_shader = createAndCompileShader('''

                #version 120
                varying vec2 st;
                void main() {
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                    st = gl_MultiTexCoord0.st;
                }
                ''',GL_VERTEX_SHADER)
        frag_shader = createAndCompileShader('''
                #version 120
                uniform sampler2D bg;
                uniform sampler2D fg;
                uniform vec3 color;
                varying vec2 st;
                void main() {
                    vec4 bgcol = texture2D(bg,st);
                    vec4 fgcol = texture2D(fg,st);
                    if(length(fgcol.xyz) == 0) {
                    gl_FragColor = bgcol;
                    } else {
                    gl_FragColor = fgcol;
                    }
                }
                ''',GL_FRAGMENT_SHADER)
        self.final_shader =glCreateProgram()
        glAttachShader(self.final_shader,vert_shader)
        glAttachShader(self.final_shader,frag_shader)
        glLinkProgram(self.final_shader)
        
    def createBackground(self):
        self.render_to_fbo(self.bg_fbo, self.drawBackground)
        
    def drawBackground(self):

        glUseProgram(self.player_shader)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        num_split = 10
        dx = 1.0 / num_split
        color_location = glGetUniformLocation(self.player_shader, "color")
        for i in xrange(num_split):
            color = game.get_game().entity_manager.get_by_name('player' + str(1+(i%2))).color
            col = map(lambda x: x/255.0, color)

            glUniform3f(color_location, col[0],col[1],col[2])
            self.drawUVQuad(i*dx,0,dx,1)

        glUseProgram(0)



    def resize(self,tup):
        x,y = tup
        self.x = x
        self.y = y
        glViewport(0,0,x,y)
        glUseProgram(self.player_shader)
        loc = glGetUniformLocation(self.player_shader,"aspectRatio")
        ratio = float(x)/y
        glUniform1f(loc,ratio)
        glUseProgram(0)

    
    def drawCircle(self,x,y,rad):
        x = float(x) / self.x
        y = float(y) / self.x
        rad = float(rad) / self.x
        glBegin(GL_TRIANGLE_FAN)
        num_div = 30
        dx = 2.0/(num_div-1) * math.pi
        for i in xrange(num_div):
            glVertex2f(x+math.cos(dx * i) * rad, y + math.sin(dx * i) * rad)
        glEnd()

    
    def drawUVQuad(self,x,y,w,h):
        glBegin(GL_QUADS)
        glVertex2f(x,y)
        glVertex2f(x,y+h)
        glVertex2f(x+w,y+h)
        glVertex2f(x+w,y)
        glEnd()

    def drawRect(self,x,y,w,h):
        x = float(x) / self.x
        y = float(y) / self.y
        w = float(w) / self.x
        h = float(h) / self.y
        self.drawUVQuad(x,y,w,h)



    def render_ss_quad(self, layer=0):
        glBegin(GL_QUADS)

        glTexCoord2f(0, 1); glVertex3f( 0, 0,layer )
        glTexCoord2f(1, 1); glVertex3f( 1, 0,layer )
        glTexCoord2f(1, 0); glVertex3f( 1, 1,layer)
        glTexCoord2f(0, 0); glVertex3f( 0, 1,layer)

        glEnd()

    def render_final_fbo(self):
        glViewport(0, 0, self.x,self.y)
        glUseProgram(self.final_shader)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)

        bgloc = glGetUniformLocation(self.final_shader, "bg")
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.bg_fbo.gl_tex_id)
        glUniform1i(bgloc,0)

        fgloc = glGetUniformLocation(self.final_shader, "fg")
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.fbo.gl_tex_id)
        glUniform1i(fgloc,1)
        self.render_ss_quad()

        glDisable(GL_TEXTURE_2D)    



    def render_fbo(self,fbo, layer=0):
        glViewport(0, 0, self.x,self.y)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1, 1, 1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, fbo.gl_tex_id)
        self.render_ss_quad(layer)

        glDisable(GL_TEXTURE_2D)    

#     def render_players(self):
#         glClearColor(0,0,0,0)
#         #glClear(GL_COLOR_BUFFER_BIT)
#         glUseProgram(self.player_shader)
#         #for view in self.views:
#         #    view.draw()
#         glColor3f(1,1,1);
# 
#         em = game.get_game().entity_manager
# 
# 
#         color_location = glGetUniformLocation(self.player_shader, "color")
#         for ent in em.get_by_tag('draw_as_player'):
#             
#             col = map(lambda x: x/255.0, ent.color)
# 
#             glUniform3f(color_location, col[0],col[1],col[2])
#             self.drawCircle(ent.x,ent.y,ent.height/2.0)
#         glUseProgram(0)

    def render_to_fbo(self,fbo, func):
        fbo.bind()
        func()
        fbo.unbind()

    def render_actions(self):
        glUseProgram(self.player_shader)
        #for view in self.views:
        #    view.draw()
        glColor3f(1,1,1);


        color_location = glGetUniformLocation(self.player_shader, "color")
            
        for item in self.draw_queue:
            (a,v) = item
            if a==0:
                color,cx,cy,r = v
                col = map(lambda x: x/255.0, color)

                glUniform3f(color_location, col[0],col[1],col[2])
                self.drawCircle(cx,cy,r)
            elif a==1:
                color,x,y,w,h = v
                col = map(lambda x: x/255.0, color)

                glUniform3f(color_location, col[0],col[1],col[2])
                self.drawRect(x,y,w,h)

        glUseProgram(0)
        
        self.draw_queue = []

    def appendCircle(self,color, px, py, rad):
        self.draw_queue.append( (0,(color,px,py,rad) ) )

    def appendRect(self,color, px, py, w,h):
        self.draw_queue.append( (1,(color,px,py,w,h)) )




    def cleanup(self):
        self.render_to_fbo(self.fbo,self.clean)

    def clean(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)




    def render(self):
#         self.render_to_fbo(self.fbo,self.render_players)
        self.render_to_fbo(self.fbo,self.render_actions)
        #self.cleanup()
        self.render_fbo(self.bg_fbo,0)
        self.render_fbo(self.fbo,.1)
        #self.render_final_fbo()
        #glColor3f(1,1,1);
        #glBegin(GL_TRIANGLES);
        #glVertex2f(0,0);
        #glVertex2f(1,0);
        #glVertex2f(0,1);
        #glEnd();
            
