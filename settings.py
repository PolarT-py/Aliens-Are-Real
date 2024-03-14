from math import floor, sqrt, atan2, cos, sin
from pathlib import Path
assets_path = Path(__file__).parent
import pygame

pygame.init()

TILESIZE = 64


def getPlayerPosFromList(List):
    for i, row in enumerate(List):
        for j, col in enumerate(row):
            if List[i][j] == "P":
                return j, i


def getListFromLevel(Path):
    l = []
    with open(Path, "r") as f:
        for row in f:
            l.append(row.split(","))

    return l


def getListFromTileIDs(List):
    l = []

    for i, row in enumerate(List):
        for j, col in enumerate(row):
            if col == "0":
                l.append(("BarbedWire", (j, i), True, False))
            elif col == "1":
                l.append(("Barrel", (j, i), True, True))
            elif col == "2":
                l.append(("Block", (j, i), True, False))
            elif col == "3":
                l.append(("TableMiddle", (j, i), True, False))
            elif col == "4":
                l.append(("TrashBin", (j, i), True, False))
            elif col == "5":
                l.append(("TableLeft", (j, i), True, False))
            elif col == "6":
                l.append(("TableRight", (j, i), True, False))
            elif col == "7":
                l.append(("Crater", (j, i), True, False))
            elif col == "8":
                l.append(("ExplosiveBarrel", (j, i), True, False))
            elif col == "9":
                l.append(("LargeRock", (j, i), True, False))
            elif col == "10":
                l.append(("MediumRock", (j, i), True, True))
            elif col == "11":
                l.append(("PiledRock", (j, i), True, True))
            elif col == "12":
                l.append(("SmallRock", (j, i), False, True))
            elif col == "21":
                l.append(("CabinRight", (j, i), True, False))
            elif col == "22":
                l.append(("CabinTop", (j, i), True, False))
            elif col == "23":
                l.append(("CabinTopLeft", (j, i), True, False))
            elif col == "24":
                l.append(("CabinTopRight", (j, i), True, False))
            elif col == "25":
                l.append(("CabinBottom", (j, i), True, False))
            elif col == "26":
                l.append(("CabinBottomLeft", (j, i), True, False))
            elif col == "27":
                l.append(("CabinBottomRight", (j, i), True, False))
            elif col == "28":
                l.append(("CabinLeft", (j, i), True, False))
            elif col == "29":
                l.append(("CabinInside", (j, i), True, False))
            elif col == "30":
                l.append(("Campfire", (j, i), True, False))
            elif col == "41":
                l.append(("Path", (j, i), False, False))
            elif col == "42":
                l.append(("TreeStump", (j, i), True, False))
            elif col == "43":
                l.append(("TreeTop1Right", (j, i), False, True))
            elif col == "44":
                l.append(("TreeTop1Left", (j, i), False, True))
            elif col == "45":
                l.append(("TrafficCone", (j, i), True, False))
            elif col == "46":
                l.append(("CrackedBlock", (j, i), True, True))
            elif col == "47":
                l.append(("PassCodeLock", (j, i), True, False))
            elif col == "48":
                l.append(("Sign", (j, i), True, True))
            elif col == "49":
                l.append(("SingleWarnSign", (j, i), True, True))
            elif col == "50":
                l.append(("TripleWarnSign", (j, i), True, True))
            elif col == "51":
                l.append(("WasdSign", (j, i), True, True))
            elif col == "52":
                l.append(("EnterSign", (j, i), True, True))
            elif col == "53":
                l.append(("GateClosed", (j, i), True, True))
            elif col == "54":
                l.append(("GateOpenedLeft", (j, i), False, True))
            elif col == "55":
                l.append(("GetOpenedRight", (j, i), False, True))
            elif col == "56":
                l.append(("MidSign", (j, i), True, True))
            elif col == "57":
                l.append(("Door", (j, i), True, True))
            elif col == "58":
                l.append(("RedKey", (j, i), "red"))
            elif col == "59":
                l.append(("PassCodePaper", (j, i), None, None))
            elif col == "60":
                l.append(("Bomb", (j, i), None, None))
            elif col == "61":
                l.append(("BlueKey", (j, i), "blue"))
            elif col == "62":
                l.append(("GreenKey", (j, i), "green"))
            elif col == "63":
                l.append(("Alien", (j, i)))

    return l


def getSurfaceFromList(List):
    surface = pygame.surface.Surface((len(List[0]) * TILESIZE, len(List) * TILESIZE), pygame.SRCALPHA)
    for i, row in enumerate(List):
        for j, col in enumerate(row):
            if col == "1":
                surface.blit(images["block"], (j * TILESIZE, i * TILESIZE))

    return surface


def doubleSurfaceSize(surface):
    return pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2)).convert_alpha()


def surfaceX4(surface):
    return doubleSurfaceSize(doubleSurfaceSize(surface))


def tileSized(surface):
    return pygame.transform.scale(surface, (TILESIZE, TILESIZE))


def getTransRect(obj, color, widthbuff=1, heightshrinkbuff=1):
    transparent_surf = pygame.Surface((obj.img.get_width() // widthbuff, obj.img.get_height() // heightshrinkbuff),
                                      pygame.SRCALPHA)
    pygame.draw.rect(transparent_surf, color, (0, 0, obj.rect[2], obj.rect[3]))
    return transparent_surf


def toWorldCoords(x, y):
    return x / TILESIZE, y / TILESIZE


def toTileCoords(x, y):
    return x * TILESIZE, y * TILESIZE


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


FPS = 600
screen_data = {
    "size": (1000, 600),
    "width": 1000,
    "halfwidth": 500,
    "height": 600,
    "halfheight": 300,
}
mainscreen = pygame.display.set_mode((screen_data["size"]), pygame.RESIZABLE)
pygame.display.set_caption("Loading assets...")
images = {
    "bg": surfaceX4(pygame.image.load(assets_path / "assets/images/backdrops/bg.png")),
    "bg1": (pygame.image.load(assets_path / "assets/images/backdrops/bg1.png")),
    "bg2": surfaceX4(pygame.image.load(assets_path / "assets/images/backdrops/bg2.png")),
    "block": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/block.png")),
    "barrel": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/barrel.png")),
    "explosive_barrel": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/explosive_barrel.png")),
    "barbed_wire": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/barbed_wire.png")),
    "crater": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/crater.png")),
    "large_rock": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/large_rock.png")),
    "medium_rock": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/medium_rock.png")),
    "small_rock": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/small_rock.png")),
    "piled_rock": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/piled_rock.png")),
    "tableleft": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/table1.png")),
    "tableright": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/table2.png")),
    "tablemiddle": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/table3.png")),
    "trashbin": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/trashbin.png")),
    "cabin_top": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_top.png")),
    "cabin_bottom": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_bottom.png")),
    "cabin_left": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_left.png")),
    "cabin_right": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_right.png")),
    "cabin_top_left": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_top_left.png")),
    "cabin_top_right": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_top_right.png")),
    "cabin_bottom_left": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_bottom_left.png")),
    "cabin_bottom_right": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_bottom_right.png")),
    "cabin_inside": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/cabin_inside.png")),
    "campfire1": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/campfire_1.png")),
    "campfire2": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/campfire_2.png")),
    "path": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/path.png")),
    "tree_stump": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/tree_stump.png")),
    "treetop_1_left": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/treetop_1_left.png")),
    "treetop_1_right": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/treetop_1_right.png")),
    "traffic_cone": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/traffic_cone.png")),
    "crackedblock": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/crackedblock.png")),
    "door": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/door.png")),
    "enter_sign": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/enter_sign.png")),
    "gate_closed": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/gate_closed.png")),
    "gate_opened_right": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/gate_opened_right.png")),
    "gate_opened_left": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/gate_opened_left.png")),
    "mid_sign": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/mid_sign.png")),
    "passcode_lock": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/passcode_lock.png")),
    "sign": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/sign.png")),
    "single_warn_sign": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/single_warn_sign.png")),
    "triple_warn_sign": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/triple_warn_sign.png")),
    "wasd_sign": surfaceX4(pygame.image.load(assets_path / "assets/images/tiles/wasd_sign.png")),

    "key_red": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/key_red.png")),
    "key_green": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/key_green.png")),
    "key_blue": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/key_blue.png")),
    "bomb": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/bomb.png")),
    "bomb_ignited": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/bomb_ignited.png")),
    "passcode_paper": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/passcode_paper.png")),
    "dialog": pygame.image.load(assets_path / "assets/images/misc/dialog.png"),
    "player_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/player_0.png")),
    "jack": surfaceX4(pygame.image.load(assets_path / "assets/images/player/friend_jack.png")),
    "josh": surfaceX4(pygame.image.load(assets_path / "assets/images/player/friend_josh.png")),
    "jack2": surfaceX4(pygame.image.load(assets_path / "assets/images/player/friend_jack2.png")),
    "player_right_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/player_right_0.png")),
    "player_right_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/player_right_1.png")),
    "player_left_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/player_left_0.png")),
    "player_left_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/player_left_1.png")),
    "jack_right_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/jack_right_0.png")),
    "jack_right_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/jack_right_1.png")),
    "jack_left_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/jack_left_0.png")),
    "jack_left_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/jack_left_1.png")),
    "josh_right_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/josh_right_0.png")),
    "josh_right_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/josh_right_1.png")),
    "josh_left_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/josh_left_0.png")),
    "josh_left_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/josh_left_1.png")),
    "guard_right_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/guard_right_0.png")),
    "guard_right_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/guard_right_1.png")),
    "guard_left_0": surfaceX4(pygame.image.load(assets_path / "assets/images/player/guard_left_0.png")),
    "guard_left_1": surfaceX4(pygame.image.load(assets_path / "assets/images/player/guard_left_1.png")),
    "guard_sleep_right": surfaceX4(pygame.image.load(assets_path / "assets/images/player/guard_sleep_right.png")),
    "guard_sleep_left": surfaceX4(pygame.image.load(assets_path / "assets/images/player/guard_sleep_left.png")),
    "alien": surfaceX4(pygame.image.load(assets_path / "assets/images/player/alien.png")),
    "explosion1": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/explosion/1.png")),
    "explosion2": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/explosion/2.png")),
    "explosion3": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/explosion/3.png")),
    "explosion4": surfaceX4(pygame.image.load(assets_path / "assets/images/misc/explosion/4.png")),
}
audio = {
    "NoobTune": assets_path / "assets/audio/music/NoobTune (Royalty Free!).ogg",
}
DEFAULTMAP = "assets/maps/aap1.5.csv"
JOEMSG = "Joe (You)"
JOSHMSG = "Josh (Friend)"
JACKMSG = "Jack (Friend)"
GUARDMSG = "Guard (Guard)"
# Some rects for scenes
CAMP_RECT = pygame.rect.Rect((toTileCoords(0, 86)[0], toTileCoords(0, 86)[1], toTileCoords(26, 100)[0], toTileCoords(26, 100)[1]))
GUARDS_SLEEPING_RECT = pygame.rect.Rect((toTileCoords(13, 33)[0], toTileCoords(13, 33)[1], toTileCoords(5, 3)[0], toTileCoords(5, 3)[1]))
GUARDS_WAKE_UP_RECT = pygame.rect.Rect((toTileCoords(13, 28)[0], toTileCoords(13, 28)[1], toTileCoords(2, 3)[0], toTileCoords(2, 3)[1]))
GUARDS_GET_BLOCKED_RECT = pygame.rect.Rect((toTileCoords(10, 28)[0], toTileCoords(10, 28)[1], toTileCoords(1, 4)[0], toTileCoords(1, 4)[1]))
DEFAULTOBJECTS = [
    ## TILE CLASS, POS, HASCOLLISION, CANBREAK
    # Layer 1
    ("TestTile", (2, 1), True, False),
    ("TestTile", (2, 2), True, False),
    ("TestTile", (2, 3), True, False),
    ("TestTile", (2, 4), True, False),
    ("TestTile", (2, 5), True, False),

    ("TestTile", (2, 1), True, False),
    ("TestTile", (2, 2), True, False),
    ("TestTile", (2, 3), True, False),
    ("TestTile", (2, 4), True, False),
    ("TestTile", (2, 5), True, False),

    ("TestTile", (3, 5), True, False),
    ("TestTile", (4, 5), True, False),
    ("TestTile", (5, 5), True, False),
    ("TestTile", (6, 5), True, False),
    ("TestTile", (7, 5), True, False),
    ("TestTile", (8, 5), True, False),
    ("TestTile", (9, 5), True, False),

    ("TestTile", (3, 1), True, False),
    ("TestTile", (4, 1), True, False),
    ("TestTile", (5, 1), True, False),
    ("TestTile", (6, 1), True, False),
    ("TestTile", (7, 1), True, False),
    ("TestTile", (8, 1), True, False),
    ("TestTile", (9, 1), True, False),
    # Layer 2
    # Layer 3
]
# Fonts
fonts = {
    "PTF": assets_path / "assets/fonts/PTF.ttf",
}
font30 = pygame.font.Font(None, 30)  # PTF font I made not good
