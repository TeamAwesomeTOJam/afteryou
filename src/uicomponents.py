import pygame
import game
from component import verify_attrs, end_round


class DrawScoreComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['target', 'x', 'y', 'direction', 'width', 'height'])
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


class DrawTimerComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['time_limit', ('time_remaining', entity.time_limit), 'x', 'y', 'width', 'height'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface, transform):
        ratio = entity.time_remaining / entity.time_limit
        remaining_rect = pygame.Rect(entity.x, entity.y, int(entity.width * ratio), entity.height)
        full_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        
        pygame.draw.rect(surface, (0,0,0), full_rect)
        pygame.draw.rect(surface, (200,200,200), remaining_rect)
    

class UpdateTimerComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['time_limit', ('time_remaining', entity.time_limit), 'x', 'y', 'width', 'height'])
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
        
    def handle_update(self, entity, dt):
        entity.time_remaining -= dt
        if entity.time_remaining < 0:
            end_round()
        