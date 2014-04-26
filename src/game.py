import sys
import pygame

import componentmanager
from entitymanager import EntityManager
from resourcemanager import ResourceManager, LoadEntityData, LoadImage, LoadInputMapping, LoadSound
from component import (AnimationComponent,
                       MovementComponent,
                       ExampleComponent, 
                       InputMovementComponent, 
                       DrawComponent, 
                       DrawHitBoxComponent,
                       PlayerCollisionComponent)

from graphicscomponents import DrawCircleComponent

from gamecomponents import SmokeScreenComponent, DecoyMovementComponent, SelfDestructComponent, SpawnDecoyComponent

from entity import Entity

from render import View, BackgroundLayer, SimpleLayer
from input import InputManager


_game = None


class Game(object):
    
    def __init__(self, screen_size, resource_path):
        global _game
        _game = self
        
        self.mode = None
        self.screen_size = screen_size

        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        
        self.component_manager = componentmanager.ComponentManager()
        self.component_manager.register_component('MovementComponent', MovementComponent())
        self.component_manager.register_component('ExampleComponent', ExampleComponent())
        self.component_manager.register_component('AnimationComponent', AnimationComponent())
        self.component_manager.register_component('DrawComponent', DrawComponent())
        self.component_manager.register_component('InputMovementComponent', InputMovementComponent())
        self.component_manager.register_component('DrawHitBoxComponent', DrawHitBoxComponent()) 
        self.component_manager.register_component('DrawCircleComponent', DrawCircleComponent())
        self.component_manager.register_component('SmokeScreenComponent', SmokeScreenComponent())
        self.component_manager.register_component('PlayerCollisionComponent', PlayerCollisionComponent())
        self.component_manager.register_component('DecoyMovementComponent', DecoyMovementComponent())
        self.component_manager.register_component('SelfDestructComponent', SelfDestructComponent())
        self.component_manager.register_component('SpawnDecoyComponent', SpawnDecoyComponent())
        
        self.entity_manager = EntityManager()
            
        self.resource_manager = ResourceManager(resource_path)
        self.resource_manager.register_loader('data', LoadEntityData)
        self.resource_manager.register_loader('image', LoadImage)
        self.resource_manager.register_loader('inputmap', LoadInputMapping)
        self.resource_manager.register_loader('sound', LoadSound)

        self.input_manager = InputManager()

        self.background_view = View(self.screen, pygame.Rect(0, 0, *self.screen_size), [BackgroundLayer()])
        self.view = View(self.screen, pygame.Rect(0, 0, *self.screen_size), [SimpleLayer('draw'), SimpleLayer('ui')])
        
    def run(self, mode):
        p1 = Entity("player1")
        p2 = Entity("player2")
        self.entity_manager.add_entity(p1)
        self.entity_manager.add_entity(p2)
        
        self.background_view.draw()

        self.mode = mode

        while True:
            dt = self.clock.tick(60) / 1000.0
            
            events = self.input_manager.process_events()
            for event in events:
                if event.target == 'GAME':
                    if event.action == 'QUIT' and event.value > 0:
                        sys.exit()
                    elif event.action == 'FULLSCREEN' and event.value > 0:
                        pygame.display.toggle_fullscreen()
                    elif event.action == 'RELOAD' and event.value > 0:
                        self.resource_manager.clear()
                else:
                    self.mode.handle_event(event)
            
            self.mode.update(dt)
            self.mode.draw()
            
            self.entity_manager.cleanup()
            
            pygame.display.flip()
            pygame.display.set_caption('fps: %.0d' % self.clock.get_fps())
            

def get_game():
    return _game
