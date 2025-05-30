from typing import Tuple

import numpy as np


# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg","3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)

#if the template doesn't do this, remove this when creating a tile status of visible/explored/shrouded
# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter. why the heck would this ever be good practice?!
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

floor = new_tile(
    walkable=True, 
    transparent=True, 
    dark=(ord(" "), 
          (255, 255, 255), #white, color of char, which is space, which makes this value irrelevant
          (50, 50, 150)), #blue/purplish
    light=(ord(" "), 
           (255,255,255), #white, color of char, which is space, which makes this value irrelevant
           (200,180, 50)), #yellow
)
wall = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord(" "), 
          (255, 255, 255), ##white, color of char, which is space, which makes this value irrelevant
          (0, 0, 100)), #dark blue
    light=(ord(" "), #tile char, space
           (255, 255,255), #white, color of char, which is space, which makes this value irrelevant
           (130, 110,50)), #brownish, 
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0,0,100), (50,50,150)),
    light=(ord(">"), (255,255,255), (200,180,50))
)






