import pygame
from component import verify_attrs


class DrawCircleComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'color', 'radius'])
        
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface, transform):
        center = transform(entity.x, entity.y)
        pygame.draw.circle(surface, entity.color, center, entity.radius)