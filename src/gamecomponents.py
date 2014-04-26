import game
import pygame
from component import verify_attrs

class SmokeScreenComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['color', 'x', 'y'])
        entity.register_handler('input', self.handle_input)
 
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
    
    def handle_input(self, entity, event):
        if event.action == 'SMOKE_SCREEN' and event.value:
            pygame.draw.circle(game.get_game().screen, entity.color, (int(entity.x), int(entity.y)), 200)
             
