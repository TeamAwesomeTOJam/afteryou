import game


class PlayMode(object):
    
    def handle_event(self, event):
        for entity in game.get_game().entity_manager.get_by_tag('input'):
            entity.handle('input', event)
            
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('update'):
            entity.handle('update', dt)
            
    def draw(self):
        for entity in game.get_game().entity_manager.get_by_tag('draw'):
            entity.handle('draw', game.get_game().screen, lambda x, y : (x, y))
