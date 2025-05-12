import tcod

from engine import Engine
from game_map import GameMap
from input_handlers import EventHandler
from entity import Entity



#dynamic screen size
screen_width = 80
screen_height = 50

FLAGS = tcod.context.SDL_WINDOW_RESIZABLE | tcod.context.SDL_WINDOW_MAXIMIZED
def main() -> None: 

    map_width = 80
    map_height = 45

    #initialize relevant variables
    event_handler = EventHandler()
    player = Entity(int(screen_width/2), int(screen_height/2), "@", (255,255,255))
    npc = Entity(int(screen_width/2-5), int(screen_height/2), "@", (255,255,0))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)
    engine = Engine(entities=entities, event_handler=event_handler,game_map=game_map, player=player)
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

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()