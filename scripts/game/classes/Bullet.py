from copy import copy

import pygame.transform

from scripts.framework.environment import *
from scripts.framework.math.Vector2 import Vector2

from scripts.game.classes.BulletData import BulletData


class Bullet:
    def __init__(self, bulletData: BulletData,  position: Vector2, angle: float, speed: float, angularSpeed=0):
        self.spritesheet = bulletData.spritesheet

        spritesheet = []
        for i in range(len(self.spritesheet)):
            sprite = self.spritesheet[i]
            newSprite = pygame.sprite.Sprite()
            newSprite.image = pygame.transform.rotate(sprite, angle)
            newSprite.rect = newSprite.image.get_rect()
            spritesheet.append(newSprite)

        self.spritesheet = spritesheet

        self.position: Vector2 = position
        self.collider = copy(bulletData.collider)

        self.angle: float = angle
        self.speed: float = speed
        self.angularSpeed: float = angularSpeed

        self.currentSprite = 0
        self.changeSpriteTimer = 0
        self.animationSpeed = bulletData.animationSpeed

    def velocity(self) -> Vector2:
        return (Vector2.up() * self.speed).rotate(self.angle)

    def move(self, deltaTime) -> bool:
        self.position += self.velocity() * deltaTime

        self.collider.position = self.position + \
            self.collider.offset.rotate(self.angle)

        self.angle += self.angularSpeed * deltaTime
        sprite = self.getSprite()
        if (self.position.x() - sprite.rect.w // 2 < GAME_ZONE[0] - 50 or
            self.position.y() - sprite.rect.h // 2 < GAME_ZONE[1] - 50) or \
                (self.position.x() + sprite.rect.w // 2 > GAME_ZONE[0] + GAME_ZONE[2] + 50 or
                 self.position.y() + sprite.rect.h // 2 > GAME_ZONE[1] + GAME_ZONE[3] + 50):
            del self
            return False
        return True

    def nextSprite(self) -> None:
        self.changeSpriteTimer += 1
        if self.changeSpriteTimer == FPS - self.animationSpeed:
            self.currentSprite = (self.currentSprite +
                                  1) % self.spritesheet.length
            self.changeSpriteTimer = 0

    def getSprite(self) -> pygame.sprite.Sprite:
        sprite = self.spritesheet[self.currentSprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite
