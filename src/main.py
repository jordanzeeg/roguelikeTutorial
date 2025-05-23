import tcod
import copy

from engine import Engine
from game_map import GameMap
from entity import Entity


from procgen import generate_dungeon
import entity_factories


#dynamic screen size
screen_width = 80
screen_height = 50

FLAGS = tcod.context.SDL_WINDOW_RESIZABLE | tcod.context.SDL_WINDOW_MAXIMIZED
def main() -> None: 

    map_width = 80
    map_height = 45

    #room variables, would make sense to add to the future levels.py file 
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2

    
    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)
    engine.game_map = generate_dungeon(max_rooms=max_rooms, 
                                room_max_size=room_max_size,
                                room_min_size=room_min_size,
                                map_width =map_width, 
                                map_height=map_height,
                                max_monsters_per_room=max_monsters_per_room,
                                engine= engine)
    
    engine.update_fov()

    #what are 32 and 8?
    tileset = tcod.tileset.load_tilesheet("assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset = tileset,
        vsync = True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order = "F")

        #game loop, everything before this can be considered initialization stuff
        while True:
            engine.render(console= root_console, context= context)

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()