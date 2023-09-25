import pygame
from os.path import join as path_join

from scripts.framework.environment import GAME_ZONE, musicModule
from scripts.framework.math.Collider import Collider
from scripts.framework.math.Vector2 import Vector2

from scripts.game.classes.Player import Player


class Item:
    def __init__(self, position: Vector2, sprite: pygame.Surface, collider: Collider, onCollect: callable, homing: bool = False):
        self.position = position
        self.startPosition = position
        self.sprite: pygame.Surface = sprite
        self.collider: Collider = collider
        self.onCollect: callable = onCollect

        self.homing = homing

        self.t = -10

    def move(self, deltaTime, player: Player) -> bool:
        if not self.homing:
            self.t += 10 * deltaTime
            self.position = Vector2(self.startPosition.x(
            ), self.startPosition.y() + (self.t ** 2 - 100))
        else:
            self.t += 60 * deltaTime
            if self.t > 1.5:
                player_pos = player.position
                direction = player_pos - self.position
                self.position += direction.normalize() * 500 * deltaTime

        self.collider.position = self.position
        if self.position.y() > GAME_ZONE[1] + GAME_ZONE[3]:
            del self
            return False
        return True

    def getSprite(self) -> pygame.sprite.Sprite:
        sprite = pygame.sprite.Sprite()
        sprite.image = self.sprite
        sprite.rect = self.sprite.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite


class PowerItem(Item):
    def __init__(self, position: Vector2, large: bool, homing: bool = False):
        if large:
            sprite = pygame.image.load(path_join(
                "assets", "sprites", "items", "power_item_large.png"))
            collider = Collider(12)
            onCollect = self.onCollect_large
        else:
            sprite = pygame.image.load(path_join(
                "assets", "sprites", "items", "power_item_small.png"))
            collider = Collider(10)
            onCollect = self.onCollect_small

        super().__init__(position, sprite, collider, onCollect, homing)

    def onCollect_large(self, player: Player):
        musicModule.sounds[20](.1)
        player.addPower(0.02)
        player.points += 10

    def onCollect_small(self, player: Player):
        musicModule.sounds[20](.2)
        player.addPower(0.005)
        player.points += 10


class PointItem(Item):
    def __init__(self, position: Vector2, homing: bool = False):
        sprite = pygame.image.load(
            path_join("assets", "sprites", "items", "point_item.png"))
        collider = Collider(10)
        onCollect = self.onCollect

        super().__init__(position, sprite, collider, onCollect, homing)

    def onCollect(self, player: Player):
        player.points += 30000 + \
            int(70000 * (GAME_ZONE[3] + GAME_ZONE[1] -
                self.position.y()) / GAME_ZONE[3])


class FullPowerItem(Item):
    def __init__(self, position: Vector2, homing: bool = False):
        sprite = pygame.image.load(
            path_join("assets", "sprites", "items", "full_power_item.png"))
        collider = Collider(12)
        onCollect = self.onCollect

        super().__init__(position, sprite, collider, onCollect, homing)

    def onCollect(self, player: Player):
        player.addPower(4)


class OneUpItem(Item):
    def __init__(self, position: Vector2, homing: bool = False):
        sprite = pygame.image.load(
            path_join("assets", "sprites", "items", "1up_item.png"))
        collider = Collider(12)
        onCollect = self.onCollect

        super().__init__(position, sprite, collider, onCollect, homing)

    def onCollect(self, player: Player):
        musicModule.sounds[5](.1)
        player.hp += 1


class StarItem(Item):
    def __init__(self, position: Vector2):
        sprite = pygame.image.load(
            path_join("assets", "sprites", "items", "star_item.png"))
        collider = Collider(10)
        onCollect = self.onCollect

        super().__init__(position, sprite, collider, onCollect, True)

    def onCollect(self, player: Player):
        player.points += 200
