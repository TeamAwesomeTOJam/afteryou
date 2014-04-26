import pygame
import game


class ChasingPlayerComponent(object):
    
    def add(self, entity):
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
    
    def handle_draw(self, entity, surface, transform):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(int(entity.x), int(entity.y), 40, 20))
        
        if game.get_game().entity_manager.get_by_name('player1').chasing:
            pass
