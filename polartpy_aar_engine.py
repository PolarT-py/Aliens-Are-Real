import sys

import pygame.key

from settings import *
from clock import *


class Engine:
    def __init__(self):
        self.running = True
        self.screen = mainscreen
        self.Clock = pygame.time.Clock()
        self.camera = self.Camera(toTileCoords(-15, -91))
        self.dt = 0.01

        self.DEBUGMODE = False
        self.scene = self.Scenes()
        self.player = self.Player(toTileCoords(15, 91))
        self.player_keys = 0
        self.player_bombs = 0
        self.player_gotpasscode = False
        self.player_bomb_delay = Timer(FPS)
        # self.player = self.Player(toTileCoords(getPlayerPosFromList()))
        self.camera.SMOOTH = False
        self.camera.goto(self.player, centered=True, offset=(self.player.img.get_width() // 2, self.player.img.get_height() // 2))  # Instantly go to player
        self.camera.SMOOTH = True
        self.npcs = [
            self.NPC(toTileCoords(13, 90), "josh"),
            self.NPC(toTileCoords(16, 91), "jack"),
            self.NPC(toTileCoords(15, 34), "guard", direction="right", sleeping=True),
            self.NPC(toTileCoords(17, 34), "guard", direction="left", sleeping=True),
        ]
        self.tiles = [
            # self.TestTile(toScreenCoords(2, 1)),
            # self.TestTile(toScreenCoords(2, 2)),
            # self.TestTile(toScreenCoords(2, 4)),
            # self.TestTile(toScreenCoords(2, 5)),
        ]
        self.items = [
            # self.Key(toTileCoords(15, 88))
        ]
        self.activebombs = [

        ]
        self.explosions = [
            # self.Explosion(toTileCoords(10, 86))
        ]
        self.SUPERMODE = False
        self.UPDATABLETILES = (self.ExplosiveBarrel, self.CampFire, self.GateClosed, self.Alien, self.PassCodeLock)
        self.load_music("NoobTune")
        pygame.mixer.music.set_volume(0.1)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def load_music(self, music, loop=-1):
        pygame.mixer.music.load(audio[music])
        pygame.mixer.music.play(loops=loop)

    def load_scene(self, scene, loadtiles=False):
        if scene == 0:
            self.scene.load_s0()
        elif scene == 1000:
            self.scene.load_s0_1()
        elif scene == 1:
            self.scene.load_s1()
        elif scene == 2:
            self.scene.load_s2()
        elif scene == 3:
            self.scene.load_s3()
        elif scene == 4:
            self.scene.load_s4()
        elif scene == 5:
            self.scene.load_s5()
        elif scene == 6:
            self.scene.load_s6()
        elif scene == 7:
            self.scene.load_s7()
        elif scene == 8:
            self.scene.load_s8()
        else:
            print("Failed to load scene!")
            return

        # Load tiles
        if loadtiles:
            self.tiles.clear()
            for data in self.scene.objects:
                # Tiles
                if data[0] == "Tile":
                    self.tiles.append(self.Tile(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TestTile":
                    self.tiles.append(self.TestTile(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Block":
                    self.tiles.append(self.Block(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Barrel":
                    self.tiles.append(self.Barrel(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "ExplosiveBarrel":
                    self.tiles.append(self.ExplosiveBarrel(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "BarbedWire":
                    self.tiles.append(self.BarbedWire(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Crater":
                    self.tiles.append(self.Crater(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "LargeRock":
                    self.tiles.append(self.LargeRock(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "MediumRock":
                    self.tiles.append(self.MediumRock(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "SmallRock":
                    self.tiles.append(self.SmallRock(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "PiledRock":
                    self.tiles.append(self.PiledRock(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TableLeft":
                    self.tiles.append(self.TableLeft(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TableRight":
                    self.tiles.append(self.TableRight(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TableMiddle":
                    self.tiles.append(self.TableMiddle(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TrashBin":
                    self.tiles.append(self.TrashBin(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinTop":
                    self.tiles.append(self.CabinTop(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinBottom":
                    self.tiles.append(self.CabinBottom(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinLeft":
                    self.tiles.append(self.CabinLeft(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinRight":
                    self.tiles.append(self.CabinRight(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinTopLeft":
                    self.tiles.append(self.CabinTopLeft(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinTopRight":
                    self.tiles.append(self.CabinTopRight(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinBottomLeft":
                    self.tiles.append(self.CabinBottomLeft(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinBottomRight":
                    self.tiles.append(self.CabinBottomRight(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CabinInside":
                    self.tiles.append(self.CabinInside(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Campfire":
                    self.tiles.append(self.CampFire(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Path":
                    self.tiles.append(self.Path(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TreeStump":
                    self.tiles.append(self.TreeStump(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TreeTop1Right":
                    self.tiles.append(self.Tree1Right(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TreeTop1Left":
                    self.tiles.append(self.Tree1Left(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TrafficCone":
                    self.tiles.append(self.TrafficCone(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "CrackedBlock":
                    self.tiles.append(self.CrackedBlock(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "PassCodeLock":
                    self.tiles.append(self.PassCodeLock(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Sign":
                    self.tiles.append(self.Sign(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "SingleWarnSign":
                    self.tiles.append(self.SingleWarnSign(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "TripleWarnSign":
                    self.tiles.append(self.TripleWarnSign(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "WasdSign":
                    self.tiles.append(self.WasdSign(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "EnterSign":
                    self.tiles.append(self.EnterSign(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "GateClosed":
                    self.tiles.append(self.GateClosed(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "GateOpenedLeft":
                    self.tiles.append(self.GateOpenedLeft(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "GateOpenedRight":
                    self.tiles.append(self.GateOpenedRight(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "MidSign":
                    self.tiles.append(self.MidSign(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Door":
                    self.tiles.append(self.Door(toTileCoords(data[1][0], data[1][1]), data[2], data[3]))
                elif data[0] == "Alien":
                    self.tiles.append(self.Alien(toTileCoords(data[1][0], data[1][1])))
                # Items
                elif data[0] in ("RedKey", "GreenKey", "BlueKey"):
                    self.items.append(self.Key(toTileCoords(data[1][0], data[1][1]), color=data[2]))
                elif data[0] == "PassCodePaper":
                    self.items.append(self.PassCodePaper(toTileCoords(data[1][0], data[1][1])))
                elif data[0] == "Bomb":
                    self.items.append(self.Bomb(toTileCoords(data[1][0], data[1][1]), thrown=False))
                else:
                    return

        l = []
        for data in self.scene.dialogs:
            if data[0] == "Dialog":
                l.append(self.Dialog(data[1], data[2], data[3], msg2=data[4], msg3=data[5]))
        self.scene.dialogs = l

    def draw(self):
        ## DRAW BACKGROUND
        self.screen.fill((0, 50, 0))
        self.screen.blit(self.scene.bg, (self.camera.x, self.camera.y))

        ## DRAW TILES & PLAYERS & NPCS  # trees need to be drawn last
        renderedstuff = self.tiles.copy()
        playerNnpcs = [self.player]
        playerNnpcs.extend(self.npcs)
        playerNnpcs = sorted(playerNnpcs, key=lambda person: person.y)
        renderedstuff.extend(playerNnpcs)
        renderedstuff.extend(self.activebombs)
        renderedstuff.extend(self.explosions)
        trees = []
        for tile in renderedstuff:
            if -(TILESIZE * 3) < self.camera.x + tile.x < screen_data["width"] + TILESIZE and -(
                    TILESIZE * 3) < self.camera.y + tile.y < screen_data["height"] + TILESIZE:  # within the screen space so won't lag (so won't draw tiles outside of screen)
                if type(tile) not in (self.Tree1Left, self.Tree1Right):
                    self.screen.blit(tile.img, (self.camera.x + tile.x, self.camera.y + tile.y))
                else:
                    trees.append(tile)

                if self.DEBUGMODE:
                    if type(tile) not in (self.Tree1Left, self.Tree1Right):
                        if type(tile) is self.Player:
                            transparent_surf = getTransRect(self.player, (0, 0, 255, 100))
                            self.screen.blit(transparent_surf, (
                            self.camera.x + self.player.rect.x, self.camera.y + self.player.rect.y))
                            transparent_surf = getTransRect(self.player, (255, 0, 255, 100), heightshrinkbuff=2)
                            self.screen.blit(transparent_surf, (
                            self.camera.x + self.player.wallrect.x, self.camera.y + self.player.wallrect.y))
                        else:
                            transparent_surf = getTransRect(tile, (0, 255, 255, 100))
                            self.screen.blit(transparent_surf, (self.camera.x + tile.rect.x, self.camera.y + tile.rect.y))

        # Draw items
        for item in self.items:
            self.screen.blit(item.img, (self.camera.x + item.x, self.camera.y + item.y))
            if self.DEBUGMODE:
                transparent_surf = getTransRect(item, (0, 255, 255, 100))
                self.screen.blit(transparent_surf, (self.camera.x + item.rect.x, self.camera.y + item.rect.y))

        for tree in trees:
            if -(TILESIZE * 3) < self.camera.x + tree.x < screen_data["width"] + TILESIZE and -(
                    TILESIZE * 3) < self.camera.y + tree.y < screen_data["height"] + TILESIZE:
                self.screen.blit(tree.img, (self.camera.x + tree.x, self.camera.y + tree.y))
                if self.DEBUGMODE:
                    transparent_surf = getTransRect(tree, (0, 255, 255, 100))
                    self.screen.blit(transparent_surf, (self.camera.x + tree.rect.x, self.camera.y + tree.rect.y))

        # pygame.draw.rect(self.screen, (50, 100, 255), (GUARDS_GET_BLOCKED_RECT[0] + self.camera.x, GUARDS_GET_BLOCKED_RECT[1] + self.camera.y, GUARDS_GET_BLOCKED_RECT[2], GUARDS_GET_BLOCKED_RECT[3]))

        ## DRAW DIALOGS
        if self.scene.reading:
            if self.scene.dialog_num >= 0 and not self.scene.dialog_num > len(self.scene.dialogs) - 1:
                self.screen.blit(self.scene.dialogs[self.scene.dialog_num].img, (100, 400))

        ## UPDATE SCREEN
        pygame.display.flip()

    def update(self):
        self.dt = self.Clock.tick(FPS) / 1000
        # pygame.display.set_caption(f"Aliens Are Real, pos {toWorldCoords(self.player.x, self.player.y)}, fps {self.Clock.get_fps()}")

        # Update Scene
        self.scene.update()

        # Update Tiles
        for tile in self.tiles:
            if type(tile) in self.UPDATABLETILES:
                if type(tile) in (self.ExplosiveBarrel, self.Alien):
                    tile.update(self.dt, tiles=self.tiles, player=self.player)

                elif type(tile) is self.CampFire:
                    tile.update(self.dt)

                elif type(tile) is self.GateClosed:
                    if tile.rect.colliderect(self.player.rect):
                        if self.player_keys >= 1:
                            self.player_keys -= 1
                            tile.dead = True
                            self.tiles.append(self.GateOpenedLeft((tile.x, tile.y + (TILESIZE * 2))))
                            self.tiles.append(self.GateOpenedRight((tile.x + (TILESIZE * 2), tile.y + (TILESIZE * 2))))

                elif type(tile) is self.PassCodeLock:
                    if tile.rect.colliderect(self.player.wallrect[0] - 10, self.player.wallrect[1], self.player.wallrect[2], self.player.wallrect[3] + 20):
                        if self.player_gotpasscode:
                            tile.dead = True

            if tile.dead:
                if tile in self.tiles:
                    if type(tile) is self.ExplosiveBarrel:
                        self.explosions.append(self.Explosion((tile.x, tile.y)))
                    self.tiles.remove(tile)

        # Update Explosions
        for explosion in self.explosions:
            explosion.update(self.dt)
            if explosion.dead:
                if explosion in self.explosions:
                    self.explosions.remove(explosion)

        # Update Player & NPCs
        self.player.update(self.dt, self.tiles, canmove=not self.scene.reading, supermode=self.SUPERMODE)
        for item in self.items:
            if self.player.wallrect.colliderect(item.rect):
                if not item.collected:
                    if type(item) is self.Key:
                        self.player_keys += 1
                        item.collected = True
                    elif type(item) is self.PassCodePaper:
                        self.player_gotpasscode = True
                        item.collected = True
                    elif type(item) is self.Bomb:
                        self.player_bombs += 1
                        item.collected = True

        # Check if throw bomb
        if self.player_bomb_delay.ring:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] and self.player_bombs >= 1:
                self.activebombs.append(self.Bomb((self.player.x - (self.player.img.get_width() // 2), self.player.y - (self.player.img.get_height() // 2)), thrown=True))
                self.player_bombs -= 1
                self.player_bomb_delay.reset()
        self.player_bomb_delay.update(self.dt)

        # Check if spawn explosion
        if self.SUPERMODE:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.tiles.append(self.ExplosiveBarrel((self.player.x, self.player.y)))

        for npc in self.npcs:
            npc.update(self.dt, self.tiles)

        # Update items
        for item in self.items:
            item.update(self.dt)
            if item.dead:
                if item in self.items:
                    self.items.remove(item)
        # Update active bombs
        for bomb in self.activebombs:
            bomb.update(self.dt, tiles=self.tiles)

            if bomb.dead:
                if bomb in self.activebombs:
                    self.explosions.append((bomb.x, bomb.y))
                    self.activebombs.remove(bomb)

    class Camera:
        def __init__(self, pos=(0, 0)):
            self.x = pos[0]
            self.y = pos[1]
            self.pos = (self.x, self.y)
            self.targetx = pos[0]
            self.targety = pos[1]
            self.SMOOTH = True
            self.SMOOTHSPEED = 0.3
            self.DEBUGMOVEMENTSPEED = 500 * 4

        def goto(self, target, centered=False, offset=(0, 0)):
            if isinstance(target, tuple):
                self.targetx, self.targety = (target[0] + offset[0] - screen_data["halfwidth"], target[1] + offset[1] - screen_data["halfheight"]) if centered else (target[0] + offset[0], target[1] + offset[1])
            else:
                self.targetx, self.targety = (target.x + offset[0] - screen_data["halfwidth"], target.y + offset[1] - screen_data["halfheight"]) if centered else (target.x + offset[0], target.y + offset[1])

        def update(self, dt, canmove):
            if (floor(self.x), floor(self.y)) != (floor(self.targetx), floor(self.targety)):
                if not self.SMOOTH:
                    self.targetx, self.targety = self.x, self.y
                else:
                    self.x -= (self.targetx + self.x) / self.SMOOTHSPEED * dt
                    self.y -= (self.targety + self.y) / self.SMOOTHSPEED * dt

            ## DEBUG MOVEMENT
            if canmove:
                key = pygame.key.get_pressed()
                if key[pygame.K_i]:
                    self.targety -= self.DEBUGMOVEMENTSPEED * dt
                elif key[pygame.K_k]:
                    self.targety += self.DEBUGMOVEMENTSPEED * dt
                if key[pygame.K_j]:
                    self.targetx -= self.DEBUGMOVEMENTSPEED * dt
                elif key[pygame.K_l]:
                    self.targetx += self.DEBUGMOVEMENTSPEED * dt

            self.pos = (self.x, self.y)

    class Player:
        def __init__(self, pos):
            self.x = pos[0]
            self.y = pos[1]
            self.dir = "right"
            self.animationframe = 0
            self.img = images["player_right_0"]
            self.halfheight = self.img.get_height() // 2
            self.rect = self.img.get_rect()
            self.wallrect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.wallrect.x = self.x
            self.wallrect.y = self.y + self.halfheight
            self.wallrect.height = self.halfheight
            self.xvel = 0
            self.yvel = 0
            self.speed = 200
            self.animationtimer = Timer(FPS // 8, start=True)
            self.pressedkey = False

        def collide_with_wall(self, direction, tiles):
            if direction == "x":
                for tile in tiles:
                    hits = self.wallrect.colliderect(tile.rect)
                    if tile.hascollision:
                        if hits:
                            if self.xvel > 0:
                                self.x = tile.rect.left - self.rect.width
                            if self.xvel < 0:
                                self.x = tile.rect.right
                            self.xvel = 0
                            self.wallrect.x = self.x
                            break
            if direction == "y":
                for tile in tiles:
                    hits = self.wallrect.colliderect(tile.rect)
                    if tile.hascollision:
                        if hits:
                            if self.yvel > 0:
                                self.y = tile.rect.top - self.rect.height
                            if self.yvel < 0:
                                self.y = tile.rect.bottom - self.halfheight
                            self.yvel = 0
                            self.wallrect.y = self.y + self.halfheight
                            break

        def update(self, dt, tiles, canmove=True, supermode=False):
            self.xvel, self.yvel = 0, 0
            self.pressedkey = False

            if canmove:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    self.speed = 300 if not supermode else 600
                else:
                    self.speed = 200 if not supermode else 400

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.xvel = -self.speed
                    self.dir = "left"
                    self.pressedkey = True
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.xvel = self.speed
                    self.dir = "right"
                    self.pressedkey = True
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.yvel = -self.speed
                    self.pressedkey = True
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.yvel = self.speed
                    self.pressedkey = True
                if self.xvel != 0 and self.yvel != 0:
                    self.xvel *= 0.7071
                    self.yvel *= 0.7071

            self.x += self.xvel * dt
            self.y += self.yvel * dt
            self.rect.x = self.x
            self.wallrect.x = self.x
            self.collide_with_wall("x", tiles)
            self.rect.y = self.y
            self.wallrect.y = self.y + self.halfheight
            self.collide_with_wall("y", tiles)

            self.update_animation(dt)

        def update_animation(self, dt):
            if self.pressedkey:
                self.animationtimer.update(dt)
            else:
                self.animationtimer.reset()
                self.animationframe = 0

            if self.animationtimer.ring:
                self.animationtimer.reset()
                self.animationframe += 1
                self.animationframe %= 2
            self.img = images[f"player_{self.dir}_{self.animationframe}"]

    class NPC:
        def __init__(self, pos, character, direction="right", sleeping=False):
            self.x = pos[0]
            self.y = pos[1]
            self.targetx = self.x
            self.targety = self.y
            self.dir = direction
            self.animationframe = 0
            self.character = character
            self.prevanimationString = f"{character}_{self.dir}_0"
            self.animationString = self.prevanimationString
            self.img = images[self.animationString]
            self.sleeping = sleeping
            self.halfheight = self.img.get_height() // 2
            self.rect = self.img.get_rect()
            self.wallrect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.wallrect.x = self.x
            self.wallrect.y = self.y + self.halfheight
            self.wallrect.height = self.halfheight
            self.xvel = 0
            self.yvel = 0
            self.speed = 200
            self.animationtimer = Timer(FPS // 8, start=True)
            self.pressedkey = False

        def collide_with_wall(self, direction, tiles):
            if direction == "x":
                for tile in tiles:
                    hits = self.wallrect.colliderect(tile.rect)
                    if tile.hascollision:
                        if hits:
                            if self.xvel > 0:
                                self.x = tile.rect.left - self.rect.width
                            if self.xvel < 0:
                                self.x = tile.rect.right
                            self.xvel = 0
                            self.wallrect.x = self.x
                            break
            if direction == "y":
                for tile in tiles:
                    hits = self.wallrect.colliderect(tile.rect)
                    if tile.hascollision:
                        if hits:
                            if self.yvel > 0:
                                self.y = tile.rect.top - self.rect.height
                            if self.yvel < 0:
                                self.y = tile.rect.bottom - self.halfheight
                            self.yvel = 0
                            self.wallrect.y = self.y + self.halfheight
                            break

        def update(self, dt, tiles, canmove=True, up=False, down=False, left=False, right=False, shift=False):
            self.xvel, self.yvel = 0, 0
            self.pressedkey = False

            if True:  # canmove is useless
                if shift:
                    self.speed = 300
                else:
                    self.speed = 200
#
                if left or self.x > self.targetx:
                    self.xvel = -self.speed
                    self.dir = "left"
                    self.pressedkey = True
                if right or self.x < self.targetx:
                    self.xvel = self.speed
                    self.dir = "right"
                    self.pressedkey = True
                if up or self.y > self.targety:
                    self.yvel = -self.speed
                    self.pressedkey = True
                if down or self.y < self.targety:
                    self.yvel = self.speed
                    self.pressedkey = True
                if self.xvel != 0 and self.yvel != 0:
                    self.xvel *= 0.7071
                    self.yvel *= 0.7071

            self.x += self.xvel * dt
            self.y += self.yvel * dt
            self.rect.x = self.x
            self.wallrect.x = self.x
            self.collide_with_wall("x", tiles)
            self.rect.y = self.y
            self.wallrect.y = self.y + self.halfheight
            self.collide_with_wall("y", tiles)

            if distance((self.x, 0), (self.targetx, 0)) <= self.speed * dt:
                self.x = self.targetx
            if distance((0, self.y), (0, self.targety)) <= self.speed * dt:
                self.y = self.targety

            self.update_animation(dt)

        def update_animation(self, dt):
            if not self.sleeping:
                if self.pressedkey:
                    self.animationtimer.update(dt)
                else:
                    self.animationtimer.reset()
                    self.animationframe = 0

                if self.animationtimer.ring:
                    self.animationtimer.reset()
                    self.animationframe += 1
                    self.animationframe %= 2
                self.animationString = f"{self.character}_{self.dir}_{self.animationframe}"
            else:
                self.animationString = f"{self.character}_sleep_{self.dir}"

            if self.prevanimationString != self.animationString:
                self.img = images[self.animationString]

            self.prevanimationString = self.animationString

    ## TILES
    class Tile:
        def __init__(self, pos, hascollision=True, canbreak=False):
            self.x = pos[0]
            self.y = pos[1]
            self.rect = pygame.rect.Rect((self.x, self.y, TILESIZE, TILESIZE))
            self.hascollision = hascollision
            self.canbreak = canbreak
            self.dead = False

        def update(self, dt, thing1=None, thing2=None):
            pass

    class TestTile(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["block"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class Block(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["block"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class Barrel(Tile):
        def __init__(self, pos, hascollision=True, canbreak=True):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["barrel"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            # commented out because player on top
            # halfheight = self.img.get_height() // 2
            # self.rect.height -= halfheight
            # self.rect.x = self.x
            # self.rect.y = self.y + halfheight

    class ExplosiveBarrel(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["explosive_barrel"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        def update(self, dt, tiles=None, player=None):
            if distance((self.x, self.y), (player.x, player.y)) < toTileCoords(4, 0)[0]:
                # will explode when player is 4 tiles or closer
                self.dead = True
            # remove tiles around it after explode
            if self.dead:
                for tile in tiles:
                    if distance((self.x, self.y), (tile.x, tile.y)) < toTileCoords(3, 0)[0]:
                        if tile.canbreak:
                            # tile.img = images["cabin_top"]  # for testing explosion range
                            tile.dead = True

    class BarbedWire(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["barbed_wire"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class Crater(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["crater"]
            self.x -= toTileCoords(0, 2)[0]
            self.y -= toTileCoords(0, 2)[1]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class LargeRock(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["large_rock"]
            self.x -= toTileCoords(0, 1)[0]
            self.y -= toTileCoords(0, 1)[1]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class MediumRock(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["medium_rock"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class SmallRock(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["small_rock"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class PiledRock(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["piled_rock"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class TableLeft(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["tableleft"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class TableRight(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["tableright"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class TableMiddle(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["tablemiddle"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class TrashBin(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["trashbin"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinTop(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_top"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinBottom(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_bottom"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinLeft(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_left"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinRight(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_right"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinTopLeft(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_top_left"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinTopRight(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_top_right"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinBottomLeft(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_bottom_left"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinBottomRight(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_bottom_right"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CabinInside(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["cabin_inside"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CampFire(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.frame = 1
            self.img = images[f"campfire{self.frame}"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.firetimer = Timer(FPS // 4)  # 4 times a second

        def update(self, dt, thing1=None, thing2=None):
            self.firetimer.update(dt)
            if self.firetimer.ring:
                self.firetimer.reset()
                if self.frame == 1:
                    self.frame += 1
                else:
                    self.frame = 1
                self.img = images[f"campfire{self.frame}"]

    class Path(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["path"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class TreeStump(Tile):
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["tree_stump"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class Tree1Right(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["treetop_1_right"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(3, 0)[0]
            self.y -= toTileCoords(0, 2)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    class Tree1Left(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["treetop_1_left"]
            self.rect = self.img.get_rect()
            self.x -= toTileCoords(3, 0)[0]
            self.y -= toTileCoords(0, 2)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    class TrafficCone(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["traffic_cone"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class CrackedBlock(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["crackedblock"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class PassCodeLock(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["passcode_lock"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 2)[0]
            self.y -= toTileCoords(0, 2)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    class Sign(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["sign"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 1)[0]
            self.y -= toTileCoords(0, 1)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    class SingleWarnSign(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["single_warn_sign"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 1)[0]
            self.y -= toTileCoords(0, 1)[1]
            self.rect.x = self.x + (self.img.get_width() // 4)
            self.rect.y = self.y
            self.rect.width = self.img.get_width() // 2

    class TripleWarnSign(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["triple_warn_sign"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 1)[0]
            self.y -= toTileCoords(0, 1)[1]
            self.rect.x = self.x + (self.img.get_width() // 4)
            self.rect.y = self.y
            self.rect.width = self.img.get_width() // 2

    class WasdSign(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["wasd_sign"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 1)[0]
            self.y -= toTileCoords(0, 1)[1]
            self.rect.x = self.x + (self.img.get_width() // 4)
            self.rect.y = self.y
            self.rect.width = self.img.get_width() // 2

    class EnterSign(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["enter_sign"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 1)[0]
            self.y -= toTileCoords(0, 1)[1]
            self.rect.x = self.x + (self.img.get_width() // 4)
            self.rect.y = self.y
            self.rect.width = self.img.get_width() // 2

    class GateClosed(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["gate_closed"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 2)[0]
            self.y -= toTileCoords(0, 2)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    class GateOpenedLeft(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["gate_opened_left"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 2)[0]
            self.y -= toTileCoords(0, 2)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    class GateOpenedRight(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["gate_opened_right"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 2)[0]
            self.y -= toTileCoords(0, 2)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    class MidSign(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["mid_sign"]
            self.rect = self.img.get_rect()
            self.x += toTileCoords(0, 3)[0]
            self.y -= toTileCoords(0, 3)[1]
            self.rect.x = self.x + (self.img.get_width() // 4)
            self.rect.y = self.y
            self.rect.width = self.img.get_width() // 2

    class Door(Tile):
        def __init__(self, pos, hascollision=False, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["door"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    class Alien(Tile):  # Sorry, time was running out so the Alien will be a tile that if you get close, he will disappear
        def __init__(self, pos, hascollision=True, canbreak=False):
            super().__init__(pos, hascollision, canbreak=canbreak)
            self.img = images["alien"]
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        def update(self, dt, tiles=None, player=None):
            if distance((self.x, self.y), (player.x, player.y)) < toTileCoords(4, 0)[0]:
                # will disappear when player is 4 tiles or closer
                self.dead = True

    class Scenes:
        # Scene 0:
        #   Test
        def __init__(self, current=0):
            # 0 = Follow player, 1 = Go to a certain place, 2 = Freecam
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = current
            self.dialog_num = -1
            self.dialogs = []
            self.objects = []
            self.bg = images["bg2"]
            self.reading = True

        def update(self):
            self.prevclick = self.currclick
            self.currclick = False
            if self.reading:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                    self.currclick = True

            if not self.prevclick and self.currclick:
                self.clicked = True
            else:
                self.clicked = False

            if self.reading:
                if self.clicked:
                    self.dialog_num += 1

            if self.dialog_num >= 0 and not self.dialog_num > len(self.dialogs) - 1:
                self.reading = True
            else:
                self.reading = False

        def load_s0(self):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 0
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "This is a test.", "Test person", images["player_right_0"]),
                ("Dialog", "This is a test. # 2", "Test person 2", images["player_right_1"]),
                ("Dialog", "This is a test. # 3", "Test person 3", images["player_left_0"]),
            ]
            self.objects = [
                # TILE CLASS, POS, HASCOLLISION, CANBREAK
                ("TestTile", (2, 1), True, False),
                ("TestTile", (2, 2), True, False),
                ("TestTile", (2, 4), True, False),
                ("TestTile", (2, 5), True, False),
                ("TestTile", (4, 3), False, False),
            ]
            self.bg = images["bg"]
            self.reading = True

        def load_s0_1(self):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 1
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "This is a test. # 1.1", "Test person 1.1", images["player_right_0"]),
                ("Dialog", "This is a test. # 2.1", "Test person 2.1", images["player_right_1"]),
                ("Dialog", "This is a test. # 3.1", "Test person 3.1", images["player_left_0"]),
            ]
            self.objects = [
                ## TILE CLASS, POS, HASCOLLISION, CANBREAK
                # Layer 1
                ("TestTile", (2, 1), True, False),
                ("TestTile", (2, 2), True, False),
                ("TestTile", (2, 4), True, False),
                ("TestTile", (2, 5), True, False),
                ("TestTile", (4, 3), False, False),
                ("TestTile", (4, 4), False, False),
                # Layer 2
                ("TrashBin", (2, 1), True, False)
                # Layer 3

            ]
            self.bg = images["bg1"]
            self.reading = True

        def load_s1(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 1
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "Hi, this is a message from the brain to the brain:", JOEMSG, images["player_0"], "Control using WASD or arrow keys, left/right shift to sprint,", "and Enter/Space to continue messages"),
                ("Dialog", "Guys,", JOEMSG, images["player_0"], "did you know that aliens are actually real?", ""),
                ("Dialog", "Dude... Who actually thinks that aliens are real.", JOSHMSG, images["josh"], "", ""),
                ("Dialog", "...", JACKMSG, images["jack"], "I know right!", "You must be dumb to think that aliens are real."),
                ("Dialog", "...", JOEMSG, images["player_0"], "", ""),
                ("Dialog", "Prove it then.", JOSHMSG, images["josh"], "", ""),
                ("Dialog", "Ok, I will!", JOEMSG, images["player_0"], "", ""),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

        def load_s2(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 2
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "Hey! Where are you going?", JACKMSG, images["jack"], "", ""),
                ("Dialog", "I'm going to prove that aliens are real.", JOEMSG, images["player_0"], "", ""),
                ("Dialog", "But why are you leaving the camp?", JACKMSG, images["jack"], "", ""),
                ("Dialog", "Just let him cook...", JOSHMSG, images["josh"], "", ""),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

        def load_s3(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 3
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "Come back when you got proof!", JACKMSG, images["jack"], "", ""),
                ("Dialog", "Yeah, I will! Just wait and see.", JOEMSG, images["player_0"], "(I think I remember there being a", "'hidden' path somewhere up in the forest.)"),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

        def load_s4(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 4
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "This must be Area 51...", JOEMSG, images["player_0"], "", "Looks like the guards are asleep."),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

        def load_s5(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 5
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "Oh no!", JOEMSG, images["player_0"], "", ""),
                ("Dialog", "...", GUARDMSG, images["guard_sleep_right"], "", ""),
                ("Dialog", "You really thought we were asleep?", GUARDMSG, images["guard_right_0"], "Then you were wrong!", "Hahahahaha."),
                ("Dialog", "Now prepare to face 69 years in jail!", GUARDMSG, images["guard_right_0"], "", ""),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

        def load_s6(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 6
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "Wow look at that! Barrel from the sky!", JOEMSG, images["player_0"], "", ""),
                ("Dialog", "What!", GUARDMSG, images["guard_left_0"], "", ""),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

        def load_s7(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 7
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "Look at these photos I took.", JOEMSG, images["player_0"], "", ""),
                ("Dialog", "WAIT! But how!?", JOSHMSG, images["josh"], "", "Ok, now I believe you."),
                ("Dialog", "Guess that was enough to make me believe in aliens too.", JACKMSG, images["jack"], "", ""),
                ("Dialog", "I told you guys!", JOEMSG, images["player_0"], "", ""),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

        def load_s8(self, MAP=DEFAULTMAP):
            self.prevclick = False
            self.currclick = False
            self.clicked = False
            self.cameramovetype = 0
            self.current = 8
            self.dialog_num = 0
            self.dialogs = [
                ("Dialog", "The end :)", JOEMSG, images["player_0"], "Oh yea now you have super speed + everyblock is breakable", "+ spawn Explosions using E, Enjoy!"),
                ("Dialog", "The end :)", JOEMSG, images["player_0"], "Oh yea now you have super speed + everyblock is breakable", "+ spawn Explosions using E, Enjoy!"),
            ]
            if not MAP:
                self.objects = DEFAULTOBJECTS
            else:
                self.objects = getListFromTileIDs(getListFromLevel(MAP))
            self.bg = images["bg2"]
            self.reading = True

    class Dialog:
        def __init__(self, message, name, img, msg2="", msg3=""):
            self.message = message
            self.message2 = msg2
            self.message3 = msg3
            self.name = name
            self.charimg = pygame.transform.scale(img, (140, 140)).copy().convert_alpha()
            self.img = images["dialog"].copy()
            self.img.blit(self.charimg, (10 + 5, 41 + 5))
            nameimg = font30.render(name, True, (0, 0, 0)).convert_alpha()
            self.img.blit(nameimg, (15, 15))
            messageimg = font30.render(self.message, True, (0, 0, 0)).convert_alpha()
            self.img.blit(messageimg, (200, 15))
            messageimg = font30.render(self.message2, True, (0, 0, 0)).convert_alpha()
            self.img.blit(messageimg, (200, 15 + 20))
            messageimg = font30.render(self.message3, True, (0, 0, 0)).convert_alpha()
            self.img.blit(messageimg, (200, 15 + 40))
            self.moveon = False

        # I don't think this is being used
        def update(self):
            keys = pygame.key.get_pressed()
            if any(keys):
                self.moveon = True

    class Explosion:
        def __init__(self, pos):
            self.x, self.y = pos
            self.dead = False
            self.timer = Timer(100)
            self.frame = 1
            self.img = images[f"explosion{self.frame}"]

            # position to the center of the position
            self.x -= toTileCoords(1, 1)[0]
            self.y -= toTileCoords(1, 1)[1]

        def update(self, dt):
            self.timer.update(dt)
            if self.timer.ring:
                self.timer.reset()
                self.frame += 1

            if self.frame > 4:
                self.dead = True
            else:
                self.img = images[f"explosion{self.frame}"]

    class Key:
        def __init__(self, pos, color="red"):
            self.x = pos[0]
            self.y = pos[1]
            self.yvel = 0
            self.color = color
            self.img = images[f"key_{color}"]
            self.rect = self.img.get_rect()
            self.rect.x, self.rect.y = self.x, self.y
            self.dead = False
            self.collected = False
            self.firstcollectedtick = False
            self.despawn = Timer(FPS // 6 * 5)

        def update(self, dt):
            if self.collected and not self.firstcollectedtick:
                self.firstcollectedtick = True
                self.yvel = 4

            if self.collected:
                self.y -= self.yvel
                self.yvel -= 10 * dt
                self.despawn.update(dt)

            if self.despawn.ring:
                self.dead = True

    class PassCodePaper:
        def __init__(self, pos):
            self.x = pos[0]
            self.y = pos[1]
            self.yvel = 0
            self.img = images["passcode_paper"]
            self.rect = self.img.get_rect()
            self.rect.x, self.rect.y = self.x, self.y
            self.dead = False
            self.collected = False
            self.firstcollectedtick = False
            self.despawn = Timer(FPS // 6 * 5)

        def update(self, dt):
            if self.collected and not self.firstcollectedtick:
                self.firstcollectedtick = True
                self.yvel = 4

            if self.collected:
                self.y -= self.yvel
                self.yvel -= 10 * dt
                self.despawn.update(dt)

            if self.despawn.ring:
                self.dead = True

    class Bomb:
        def __init__(self, pos, thrown=False):
            self.thrown = thrown
            if not self.thrown:  # Item form
                self.x = pos[0]
                self.y = pos[1]
                self.yvel = 0
                self.xvel = 0
                self.img = images["bomb"]
                self.rect = self.img.get_rect()
                self.rect.x, self.rect.y = self.x, self.y
                self.dead = False
                self.collected = False
                self.firstcollectedtick = False
                self.despawn = Timer(FPS // 6 * 5)
            else:  # Thrown form
                self.x = pos[0]
                self.y = pos[1]
                self.img = images["bomb_ignited"]
                self.rect = self.img.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
                self.speed = 400
                self.dead = False
                #
                mouse_x, mouse_y = pygame.mouse.get_pos()
                diff_x = mouse_x - self.rect.centerx
                diff_y = mouse_y - self.rect.centery
                angle = atan2(diff_y, diff_x)
                self.xvel = cos(angle) * self.speed
                self.yvel = sin(angle) * self.speed

        def update(self, dt, tiles=None):
            if not self.thrown:
                if self.collected and not self.firstcollectedtick:
                    self.firstcollectedtick = True
                    self.yvel = 4

                if self.collected:
                    self.y -= self.yvel
                    self.yvel -= 10 * dt
                    self.despawn.update(dt)

                if self.despawn.ring:
                    self.dead = True
            else:
                self.rect.x += self.xvel * dt
                self.rect.y += self.yvel * dt

                if tiles is not None:
                    for tile in tiles:
                        if self.rect.colliderect(tile.rect):
                            self.dead = True
