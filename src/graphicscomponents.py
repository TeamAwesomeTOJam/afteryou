import pygame
from component import verify_attrs


class DrawCircleComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'color', 'height', 'width'])
        
        entity.register_handler('draw', self.handle_draw)
    
    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface, transform):
        screen_x, screen_y = transform(entity.x, entity.y)
        r = pygame.Rect(int(screen_x), int(screen_y), entity.height, entity.width)
        pygame.draw.ellipse(surface, entity.color, r)