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


class Engine: 
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities -{self.player}:
            if entity.ai:
                entity.ai.perform()

    
    def render(self, console: Console, context: Context)-> None:
        #alter render to only clear changes maybe? 

        #render map
        self.game_map.render(console)

        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}"
        )

        context.present(console)

        console.clear()


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