import game
from component import verify_attrs
import mode


class DrawScoreComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['target', 'x', 'y', 'direction', 'width', 'height'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
    
    def handle_draw(self, entity):
        player = game.get_game().entity_manager.get_by_name(entity.target)
        radius = entity.height/2
        
        if player.chasing:
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y, entity.width, entity.height)
        else:
            game.get_game().renderer.appendRect((1,1,1), entity.x, entity.y, entity.width, entity.height)
        
        for i in range(player.score):
            if entity.direction == 1:
                start_x = entity.x + radius
            else:
                start_x = entity.x + entity.width - radius
            pos = (start_x + (i * radius * 2 * entity.direction), entity.y + radius)
            game.get_game().renderer.appendCircle(player.color, pos[0], pos[1], radius)


class DrawTimerComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['time_limit', ('time_remaining', entity.time_limit), 'x', 'y', 'width', 'height'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity):
        ratio = entity.time_remaining / entity.time_limit
        game.get_game().renderer.appendRect((1,1,1), entity.x, entity.y, entity.width, entity.height)
        game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y, entity.width * ratio, entity.height)
    

class UpdateTimerComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['time_limit', ('time_remaining', entity.time_limit), 'x', 'y', 'width', 'height'])
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
        
    def handle_update(self, entity, dt):
        entity.time_remaining -= dt
        if entity.time_remaining < 0:
            game.get_game().change_mode(mode.BetweenRoundMode())
        

class DrawActionsComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['target', 'x', 'y', 'width', 'height'])
        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)
        
    def handle_draw(self, entity, surface, transform):
        player = game.get_game().entity_manager.get_by_name(entity.target)
        if player.chasing:
            ratio = player.speed_boost_activation_cooldown / player.speed_boost_activation_cooldown_time
            game.get_game().renderer.appendRect((1,1,1), entity.x, entity.y, entity.width, entity.height/2)
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y + entity.height/2, entity.width * ratio, entity.height/2)
            
            ratio = player.minefield_cooldown / player.minefield_cooldown_time
            game.get_game().renderer.appendRect((1,1,1), entity.x, entity.y, entity.width, entity.height/2)
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y + entity.height/2, entity.width * ratio, entity.height/2)
        else:
            ratio = player.smoke_screen_cooldown / player.smoke_screen_cooldown_time
            game.get_game().renderer.appendRect((1,1,1), entity.x, entity.y, entity.width, entity.height/2)
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y + entity.height/2, entity.width * ratio, entity.height/2)
            
            ratio = player.decoy_cooldown_time / player.decoy_cooldown
            game.get_game().renderer.appendRect((1,1,1), entity.x, entity.y, entity.width, entity.height/2)
            game.get_game().renderer.appendRect((200,200,200), entity.x, entity.y + entity.height/2, entity.width * ratio, entity.height/2)
    
