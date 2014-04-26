import game
import pygame
from component import verify_attrs
from vec2d import Vec2d
from entity import Entity
from component import get_midpoint

class SmokeScreenComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['color', 'x', 'y', 'width', 'height', ('smoke_screen_cooldown', 0)])
        entity.register_handler('input', self.handle_input)
        entity.register_handler('update', self.handle_update)
 
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_input(self, entity, event):
        if event.action == 'SMOKE_SCREEN' and event.value and entity.smoke_screen_cooldown <= 0 and entity.chasing:
            p = get_midpoint(entity)
            pygame.draw.circle(game.get_game().screen, entity.color, (int(p[0]), int(p[1])), 200)
            entity.smoke_screen_cooldown = 10
    
    def handle_update(self, entity, dt):
        if entity.smoke_screen_cooldown >= 0:
            entity.smoke_screen_cooldown -= dt

class SpawnDecoyComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'dx', 'dy',('decoy_cooldown',0), 'color'])
        entity.register_handler('update', self.handle_update)
        entity.register_handler('input', self.handle_input)
    
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.decoy_cooldown >= 0:
            entity.decoy_cooldown -= dt
    
    def handle_input(self, entity, event):
        if event.action == 'CREATE_DECOY' and event.value and entity.decoy_cooldown <= 0 and entity.chasing:
            if entity.dx or entity.dy:
                d = (entity.dx,entity.dy)
            else:
                d = (1,0)
            game.get_game().entity_manager.add_entity(Entity("decoy",follow_entity = entity, color = entity.color, mirror_dir = d, x = entity.x, y = entity.y))
            entity.decoy_cooldown = 10
        
        
class DecoyMovementComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, [('dx', 0), ('dy', 0), 'follow_entity','mirror_dir'])
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        v = Vec2d(entity.follow_entity.dx, entity.follow_entity.dy)
        projection = v.projection(Vec2d(entity.mirror_dir))
        a = projection - v
        d = v +  (2 * a)
        entity.dx = d[0]
        entity.dy = d[1]

class  SelfDestructComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['liveness'])
        entity.register_handler('update', self.handle_update)
    
    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)
        
    def handle_update(self, entity, dt):
        entity.liveness -= dt
        if entity.liveness <= 0:
            game.get_game().entity_manager.remove_entity(entity)
            
class MinefieldComponent(object):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height', ('minefield_cooldown',0), 'color'])
        entity.register_handler('update', self.handle_update)
        entity.register_handler('input', self.handle_input)
    
    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)
        entity.unregister_handler('update', self.handle_update)
    
    def handle_update(self, entity, dt):
        if entity.minefield_cooldown >= 0:
            entity.minefield_cooldown -= dt
    
    def handle_input(self, entity, event):
        if event.action == 'PLACE_MINEFIELD' and event.value and entity.minefield_cooldown <= 0 and not entity.chasing:
            m = get_midpoint(entity)
            for r in range(30,250,50):
                for a in range(0,360,20):
                    v = Vec2d(0,1)
                    v.length = r
                    v.angle = a
                    p = m + v
                    pygame.draw.circle(game.get_game().screen, entity.color, (int(p[0]), int(p[1])), 5)
            entity.minefield_cooldown = 10
    
    
             
