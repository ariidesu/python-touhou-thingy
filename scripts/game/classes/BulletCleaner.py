import pygame
from os.path import join as path_join

from scripts.framework.environment import *
from scripts.framework.math.General import *
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.math.Collider import Collider


class BulletCleaner:
    def __init__(self, position: Vector2, increase_speed: int = 1000, give_points: bool = False, show_sprite: bool = True):
        self.collider = Collider(
            0,
            position
        )

        self.sprite = pygame.image.load(path_join(
            "assets", "sprites", "effects", "player_death_effect.png")).convert_alpha()

        self.increase_speed = increase_speed
        self.give_points = give_points

        self.kill = False
        self.show_sprite = show_sprite

    def update(self, bullets, scene, deltaTime):
        self.collider.radius += self.increase_speed * deltaTime

        i = 0
        while i < len(bullets):
            if bullets[i].collider.hasCollided(self.collider):
                bullet = bullets.pop(i)
                if self.give_points:
                    point_item = self.spawnPointItem(bullet.position)
                    scene.items.append(point_item)
                del bullet
                i -= 1
            i += 1

        if self.collider.radius ** 2 >= GAME_ZONE[2] ** 2 + GAME_ZONE[3] ** 2:
            self.kill = True

    def getSprite(self):
        if not self.show_sprite:
            return pygame.Surface((0, 0))
        image = pygame.transform.scale(
            self.sprite, (self.collider.radius * 2, self.collider.radius * 2))
        image.set_alpha(clamp(255 - self.collider.radius ** 2 /
                        (GAME_ZONE[2] ** 2 + GAME_ZONE[3] ** 2) * 1000, 0, 255))

        return image

    def spawnPointItem(self, position: Vector2):
        from scripts.game.classes.Item import StarItem
        return StarItem(position)
