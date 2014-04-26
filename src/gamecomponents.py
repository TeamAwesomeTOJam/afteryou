import game
import pygame
from component import verify_attrs

class SmokeScreenComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['color', 'x', 'y', ('smoke_screen_cooldown', 0)])
        entity.register_handler('input', self.handle_input)
        entity.register_handler('update', self.handle_update)
 
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
    
    def handle_input(self, entity, event):
        if event.action == 'SMOKE_SCREEN' and event.value and entity.smoke_screen_cooldown <= 0:
            pygame.draw.circle(game.get_game().screen, entity.color, (int(entity.x), int(entity.y)), 200)
            entity.smoke_screen_cooldown = 10
    
    def handle_update(self, entity, dt):
        entity.smoke_screen_cooldown -= dt
        
        
class DecoyMovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y'])
             
