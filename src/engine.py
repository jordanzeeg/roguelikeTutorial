from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov


from input_handlers import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler
from render_functions import render_bar, render_names_at_mouse_location
from message_log import MessageLog

class Engine: 
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities -{self.player}:
            if entity.ai:
                entity.ai.perform()

    
    def render(self, console: Console)-> None:
        #alter render to only clear changes maybe? 

        #render map
        self.game_map.render(console)
        #TODO create a file for ui locations
        self.message_log.render(console=console, x=81, y=0, width=40, height=50)
        
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )
        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)



    def update_fov(self)-> None:
        """recompute the visible area based on the players point of view
        literally only works for one character"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        #if a tile is "visible" it should be added to explored.
        self.game_map.explored |= self.game_map.visible
        #the above line is inefficient because it checks every element