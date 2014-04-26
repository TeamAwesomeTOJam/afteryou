import pygame
import game
from component import verify_attrs


class DrawScoreComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['target', 'x', 'y', 'direction'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
    
    def handle_draw(self, entity, surface, transform):
        player = game.get_game().entity_manager.get_by_name(entity.target)
        rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        radius = entity.height/2
        
        if player.chasing:
            pygame.draw.rect(surface, (200,200,200), rect)
        else:
            pygame.draw.rect(surface, (0,0,0), rect) 
        
        for i in range(player.score):
            if entity.direction == 1:
                start_x = entity.x + radius
            else:
                start_x = entity.x + entity.width - radius
            pos = (start_x + (i * radius * 2 * entity.direction), entity.y + radius)
            pygame.draw.circle(surface, player.color, pos, radius)
