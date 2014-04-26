import game
import pygame
from component import verify_attrs
from vec2d import Vec2d

class SmokeScreenComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['color', 'x', 'y', ('smoke_screen_cooldown', 0)])
        entity.register_handler('input', self.handle_input)
        entity.register_handler('update', self.handle_update)
 
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_input(self, entity, event):
        if event.action == 'SMOKE_SCREEN' and event.value and entity.smoke_screen_cooldown <= 0:
            pygame.draw.circle(game.get_game().screen, entity.color, (int(entity.x), int(entity.y)), 200)
            entity.smoke_screen_cooldown = 10
    
    def handle_update(self, entity, dt):
        entity.smoke_screen_cooldown -= dt
        
        
class DecoyMovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('dx', 0), ('dy', 0), 'follow_entity','mirror_dir'])
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        v = Vec2d(entity.follow_entity.dx, entity.follow_entity.dy)
        projection = v.projection(Vec2d(entity.mirror_dir))
        a = projection - v
        d = v +  (2 * a)
        entity.dx = d[0]
        entity.dy = d[1]
        
             
