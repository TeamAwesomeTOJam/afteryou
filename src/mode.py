import game
import entity


class AttractMode(object):
    
    def enter(self):
        self.music = game.get_game().resource_manager.get('sound', 'Prelude.ogg')
        self.music.play()
    
    def leave(self):
        self.music.stop()
    
    def handle_event(self, event):
        if event.action not in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            game.get_game().change_mode(PlayMode())
        
    def update(self, dt):
        pass
    
    def draw(self):
        game.get_game().renderer.render_title()
    

class PlayMode(object):

    def enter(self):
        self.music = game.get_game().resource_manager.get('sound', 'Main Body.ogg')
        self.music.play(loops=-1)
        
        game.get_game().entity_manager.add_entity(entity.Entity("vortexspawner"))
    
    def leave(self):
        player1 = game.get_game().entity_manager.get_by_name('player1')
        player2 = game.get_game().entity_manager.get_by_name('player2')
        timer = game.get_game().entity_manager.get_by_name('timer')
                
        if (player1.chasing and timer.time_remaining < 0) or (player2.chasing and timer.time_remaining >= 0):
            winner = player2
        else:
            winner = player1
            
        winner.score += 1
    
        for player in [player1, player2]:
            player.chasing = False if player.chasing else True   
            player.x = player.static.x
            player.y = player.static.y
            player.dx = 0
            player.dy = 0
            
        for decoy in game.get_game().entity_manager.get_by_tag('decoy'):
            game.get_game().entity_manager.remove_entity(decoy)
        
        for vortex in game.get_game().entity_manager.get_by_tag('vortex'):
            game.get_game().entity_manager.remove_entity(vortex)  
            
        for vortexspawner in game.get_game().entity_manager.get_by_tag('vortexspawner'):
            game.get_game().entity_manager.remove_entity(vortexspawner)          
            
        timer.time_remaining = timer.time_limit
        self.music.stop()

    def handle_event(self, event):
        entity = game.get_game().entity_manager.get_by_name(event.target)
        entity.handle('input', event)
            
    def update(self, dt):
        for entity in game.get_game().entity_manager.get_by_tag('update'):
            entity.handle('update', dt)
            
    def draw(self):
        game.get_game().view.draw()
        game.get_game().renderer.render_play()


class BetweenRoundMode(object):
    
    def __init__(self):
        self.ttl = 3
    
    def enter(self):
        self.music = game.get_game().resource_manager.get('sound', 'Drums Intro.ogg')
        self.music.play(loops=-1)
        #game.get_game().background_view.draw()
        game.get_game().renderer.cleanup()
        
    def leave(self):
        self.music.stop()
    
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        self.ttl -= dt
        if self.ttl < 0:
            game.get_game().change_mode(PlayMode())
    
    def draw(self):
        game.get_game().renderer.render_victor()
