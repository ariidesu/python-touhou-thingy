from os.path import join as path_join

import pygame.transform

from scripts.framework.environment import *
from scripts.framework.math.General import *
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.math.Collider import Collider
from scripts.framework.ui.Scene import Scene

from scripts.game.classes.BulletCleaner import BulletCleaner
from scripts.game.classes.Entity import Entity
from scripts.game.characters.data import *


class Player(Entity):
    def __init__(self, id: int, scene: Scene, hp: int):
        super().__init__()
        self.name: str = characters[id]['name']
        self.spritesheet: pygame.sprite = characters[id]['spritesheet']
        self.attackFunction: callable = characters[id]['attack-function']

        self.position: Vector2 = Vector2(
            (GAME_ZONE[2] + GAME_ZONE[0] + self.spritesheet.x) // 2, GAME_ZONE[1] + GAME_ZONE[3] - 100)
        self.speed: int = characters[id]['speed']

        self.collider = Collider(2)

        self.hitboxSprite = pygame.image.load(
            path_join("assets", "sprites", "effects", "player_hitbox.png")).convert_alpha()
        self.hitboxSprites = [pygame.transform.rotate(
            self.hitboxSprite, n) for n in range(360)]
        self.changeHitboxSpriteTimer = 0

        self.defaultSprites = [self.spritesheet[i]
                               for i in range(len(self.spritesheet))]
        self.rightSlopeSprites = [pygame.transform.rotate(
            self.spritesheet[i], 7) for i in range(len(self.spritesheet))]
        self.leftSlopeSprites = [pygame.transform.flip(
            sprite, flip_x=True, flip_y=False) for sprite in self.rightSlopeSprites]

        self.points = 0
        self.hp = hp
        self.reviving = False
        self.invincibilityTimer = 0

        self.spriteSize = Vector2(self.spritesheet.x, self.spritesheet.y)

        self.changeSpriteTimer = 0
        self.slow: bool = False

        self.attackTimer = 0
        self.power = 2.4

        self.bullets = []

        self.slowRate = Vector2.zero()

        self.scene = scene

    def update(self) -> None:
        deltaTime = self.scene.deltaTime

        if self.slow:
            self.slowRate += Vector2.one() * deltaTime
        else:
            self.slowRate += Vector2.right() * deltaTime

        if not self.reviving:
            for bullet in self.scene.enemyBullets:
                if bullet.collider.hasCollided(self.collider):
                    self.getDamage()
                    break

            for enemy in self.scene.enemies:
                if enemy.collider.hasCollided(self.collider):
                    self.getDamage()
                    break

        for item in self.scene.items:
            if item.collider.hasCollided(self.collider):
                item.onCollect(self)
                musicModule.sounds[8](.1)
                self.scene.items.remove(item)
                del item

        self.attackTimer += 2.5 * 60 * deltaTime
        self.changeSpriteTimer += 1 * 60 * deltaTime
        self.changeHitboxSpriteTimer += 1 * 60 * deltaTime
        self.nextSprite(5)

    def move(self, direction_vector: Vector2) -> None:
        sprite_rect = self.getSprite().rect

        self.spritesheet = self.defaultSprites \
            if direction_vector.x() == 0\
            else self.rightSlopeSprites if direction_vector.x() < 0\
            else self.leftSlopeSprites

        deltaTime = self.scene.deltaTime

        if self.reviving:
            self.invincibilityTimer += 1 * 60 * deltaTime
            self.position += Vector2.up() * 2 * 60 * deltaTime

            # If no HP left
            if self.hp < 0 and self.position.y() <= GAME_ZONE[3] + GAME_ZONE[1] + 40:
                self.switchToTitle()

            if self.position.y() <= GAME_ZONE[3] + GAME_ZONE[1] - 100:
                self.reviving = False
                self.invincibilityTimer = 0
        else:
            self.position = (self.position + direction_vector.normalize() * self.speed * deltaTime * (.5 if self.slow else 1)) \
                .clamp(GAME_ZONE[0] + sprite_rect.w // 2, (GAME_ZONE[2] + GAME_ZONE[0]) - sprite_rect.w // 2,
                       GAME_ZONE[1] + sprite_rect.h // 2, (GAME_ZONE[3] + GAME_ZONE[1]) - sprite_rect.h // 2)

        self.collider.position = self.position

    def shoot(self) -> None:
        if self.attackTimer >= 16:
            musicModule.sounds[17](.1)
            self.bullets += self.attackFunction(
                self.position + Vector2.up() * 10, int(self.power))
            self.attackTimer = 0

    def getDamage(self):
        musicModule.sounds[16](.2)
        self.scene.bulletCleaner = BulletCleaner(self.position)
        self.hp -= 1
        self.reviving = True
        self.position = Vector2(
            50 + (GAME_ZONE[2] - GAME_ZONE[0]) // 2, HEIGHT + 80)

    def addPower(self, power: float):
        self.power += power
        if self.power > 4:
            self.power = 4

    def getHitboxSprite(self):
        return self.hitboxSprites[clamp(int(self.changeHitboxSpriteTimer % 360), 0, len(self.hitboxSprites) - 1)]

    def switchToTitle(self):
        from scripts.game.scenes.TitleScene import TitleScene
        self.scene.switchToScene(TitleScene())
