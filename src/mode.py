import game


class AttractMode(object):
    
    def handle_event(self, event):
        if event.action not in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            game.get_game().mode = PlayMode()
        
    def update(self, dt):
        pass
    
    def draw(self):
        pass
    

class PlayMode(object):
    
    def handle_event(self, event):
        entity = game.get_game().entity_manager.get_by_name(event.target)
        entity.handle('input', event)
            
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('update'):
            entity.handle('update', dt)
            
    def draw(self):
        game.get_game().view.draw()


class BetweenRoundMode(object):
    
    def __init__(self):
        self.ttl = 3
    
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        self.ttl -= dt
        if self.ttl < 0:
            game.get_game().mode = PlayMode()
    
    def draw(self):
        pass