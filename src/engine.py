from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

import exceptions

import lzma
import pickle

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld

import render_functions

from message_log import MessageLog

class Engine: 
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.player = player
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)

    def handle_enemy_turns(self) -> None:
        for actor in set(self.game_map.actors) - {self.player}:
            if actor.ai:
                try:
                    actor.ai.perform()
                except exceptions.Impossible:
                    pass
    
    def render(self, console: Console)-> None:
        #alter render to only clear changes maybe? 

        #render map
        self.game_map.render(console)
        #TODO create a file for ui locations
        self.message_log.render(console=console, x=81, y=0, width=40, height=50)
        
        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0,47),
        )

        render_functions.render_names_at_mouse_location(console=console, x=21, y=44, engine=self)



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


    def save_as(self, filename:str)-> None:
        """save this engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)