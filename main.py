import polartpy_aar_engine as engine
from polartpy_aar_engine import pygame
import asyncio
from settings import *


class Game:
    def __init__(self):
        self.engine = engine.Engine()
        self.engine.load_scene(1, loadtiles=True)
        self.screen = self.engine.screen
        pygame.display.set_icon(images["player_0"])
        pygame.display.set_caption("Aliens Are Real")

        self.dt = 0.01

    def draw(self):
        self.engine.draw()

    def update(self):
        self.engine.update()
        dt = self.engine.dt

        if self.engine.scene.cameramovetype == 0:
            self.engine.camera.goto(self.engine.player, centered=True, offset=(self.engine.player.img.get_width() // 2, self.engine.player.img.get_height() // 2))
            self.engine.camera.update(dt, canmove=True)

        # Load scenes
        player_pos = (self.engine.player.x, self.engine.player.y)
        player_wallrect = self.engine.player.wallrect
        if not CAMP_RECT.colliderect(player_wallrect) and self.engine.scene.current == 1:
            self.engine.npcs[1].targetx -= toTileCoords(-2, 4)[0]
            self.engine.npcs[1].targety -= toTileCoords(-2, 4)[1]
            self.engine.load_scene(2)
        if self.engine.scene.current == 2 and not self.engine.scene.reading:
            self.engine.load_scene(3)
            self.engine.scene.dialog_num = 999
            self.engine.scene.reading = False
        if CAMP_RECT.colliderect(player_wallrect) and 1 < self.engine.scene.current < 6:
            self.engine.player.y -= self.engine.player.speed * dt
            self.engine.scene.dialog_num = 0
        if GUARDS_SLEEPING_RECT.colliderect(player_wallrect) and self.engine.scene.current < 4:
            self.engine.load_scene(4)
        if GUARDS_WAKE_UP_RECT.colliderect(player_wallrect) and self.engine.scene.current < 5:
            self.engine.npcs[2].sleeping = False
            self.engine.npcs[3].sleeping = False
            self.engine.npcs[2].targetx += toTileCoords(1, 3)[0]
            self.engine.npcs[2].targety -= toTileCoords(1, 3)[1]
            self.engine.npcs[3].targetx -= toTileCoords(1, 3)[0]
            self.engine.npcs[3].targety -= toTileCoords(1, 3)[1]
            self.engine.load_scene(5)
        if GUARDS_GET_BLOCKED_RECT.colliderect(player_wallrect) and self.engine.scene.current < 6:
            self.engine.npcs[2].targetx += toTileCoords(-2, 2)[0]
            self.engine.npcs[2].targety -= toTileCoords(-2, 2)[1]
            self.engine.npcs[3].targetx += toTileCoords(-3, 1)[0]
            self.engine.npcs[3].targety -= toTileCoords(-3, 1)[1]
            self.engine.load_scene(6)
            self.engine.tiles.append(self.engine.Barrel(toTileCoords(12, 30), canbreak=False))
        if CAMP_RECT.colliderect(player_wallrect) and self.engine.scene.current == 6:
            self.engine.load_scene(7)
            self.engine.scene.reading = True
            self.engine.scene.dialog_num = 0
        if not self.engine.scene.reading and self.engine.scene.current == 7:
            self.engine.load_scene(8)
            self.engine.npcs[0].targetx += toTileCoords(4, -3)[0]
            self.engine.npcs[0].targety += toTileCoords(4, -3)[1]
            self.engine.npcs[1].targetx += toTileCoords(0, 1)[0]
            self.engine.npcs[1].targety += toTileCoords(0, 1)[1]
            self.engine.SUPERMODE = True
            for tile in self.engine.tiles:
                tile.canbreak = True

        # self.engine.npcs[0].targetx, self.engine.npcs[0].targety = pygame.mouse.get_pos()[0] + self.engine.camera.x, pygame.mouse.get_pos()[1] + self.engine.camera.y

    async def main(self):
        while self.engine.running:
            self.engine.get_events()
            self.update()
            self.draw()
            await asyncio.sleep(0)


if __name__ == "__main__":
    game = Game()
    asyncio.run(game.main())
