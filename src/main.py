import tcod
import traceback


from game_map import GameMap
from entity import Entity


import exceptions
import input_handlers
import colors
import setup_game



FLAGS = tcod.context.SDL_WINDOW_RESIZABLE | tcod.context.SDL_WINDOW_MAXIMIZED



def save_game(handler: input_handlers.BaseEventHandler, filename:str)-> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved")


def main() -> None: 

    #dynamic screen size
    screen_width = 120 #was 80
    screen_height = 50

    

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

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
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), colors.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()