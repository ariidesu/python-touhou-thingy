import numpy as np
import pygame.surface

from scripts.framework.environment import musicModule
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.math.Spline import BasisSpline
from scripts.framework.ui.SpriteSheet import SpriteSheet
from scripts.framework.ui.SpriteFunctions import scaleSprite, setAlphaSprite

from scripts.game.classes.BulletCleaner import BulletCleaner
from scripts.game.classes.Effect import Effect
from scripts.game.classes.Item import *
from scripts.game.classes.Entity import Entity

BSpline = BasisSpline()


class Enemy(Entity):
    def __init__(self,
                 position: Vector2,
                 trajectory: [np.ndarray, ...],
                 speed,
                 spritesheet: SpriteSheet,
                 collider: Collider,
                 hp: int,
                 attackData: [(callable, float), ...],
                 drop,
                 clearBulletsOnDeath,
                 bulletPool,
                 scene):

        super().__init__()
        self.startPosition: Vector2 = position
        self.position: Vector2 = position
        self.trajectory = trajectory
        self.t = 0

        self.maxHp: int = hp
        self.hp: int = self.maxHp

        self.attackData: [(callable, float), ...] = attackData
        self.attack_count = 0

        self.spritesheet = spritesheet
        self.currentSprite = 0
        self.changeSpriteTimer = 10

        self.deathEffectSprite = pygame.sprite.Sprite()
        self.deathEffectSprite.image = pygame.image.load(
            path_join("assets", "sprites", "effects", "fairy_death_0.png")).convert_alpha()
        self.deathEffectSprite.rect = self.deathEffectSprite.image.get_rect()

        self.bulletSpawnSprite = pygame.sprite.Sprite()
        self.bulletSpawnSprite.image = pygame.image.load(path_join(
            "assets", "sprites", "effects", "bullet_spawn_effect.png")).convert_alpha()
        self.bulletSpawnSprite.rect = self.bulletSpawnSprite.image.get_rect()

        self.clearBulletsOnDeath = clearBulletsOnDeath

        self.bullets: list = bulletPool

        self.collider: Collider = collider
        self.drop = drop

        self.scene = scene
        self.target = scene.player

        self.speed = speed

    def move(self) -> None:
        self.collider.position = self.position + self.collider.offset

        deltaTime = self.scene.deltaTime

        self.position = Vector2(coords=BSpline.curve(
            self.trajectory, self.t)) + Vector2(GAME_ZONE[0], GAME_ZONE[1])
        self.t += self.speed * deltaTime
        if self.t > len(self.trajectory) - 1:
            self.death()

    def update(self) -> None:
        self.changeSpriteTimer += 1 * 60 * self.scene.deltaTime

        if self.attackData and self.attack_count < len(self.attackData):
            if self.t >= self.attackData[self.attack_count][1]:
                musicModule.sounds[3](.1)
                bullets = self.attackData[self.attack_count][0](
                    *self.attackData[self.attack_count][2])

                for bullet in bullets:
                    bullet.position += self.position

                if len(self.bullets) > 0:
                    self.scene.effects.append(Effect(
                        position=bullets[0].position,
                        spritesheet=[setAlphaSprite(scaleSprite(
                            self.bulletSpawnSprite, 3 - n / 2), 50 + n * 41).image for n in range(5)],
                        delay=4
                    ))

                self.bullets.extend(bullets)
                self.attack_count += 1

        self.nextSprite(4)

        for bullet in self.target.bullets:
            if self.collider.hasCollided(bullet.collider):
                self.target.points += 100
                self.getDamage(bullet.damage)
                self.target.bullets.remove(bullet)
                del bullet

    def getDamage(self, damage: int) -> None:
        musicModule.sounds[2](.2)
        self.hp -= damage
        if self.hp <= 0:
            self.death()

    def death(self):
        if self.hp <= 0:
            musicModule.sounds[23](.15)

            if self.clearBulletsOnDeath:
                self.scene.bulletCleaner = BulletCleaner(
                    self.position, give_points=True, show_sprite=False, increase_speed=2000)

            self.scene.effects.append(Effect(
                position=self.position,
                spritesheet=[setAlphaSprite(scaleSprite(
                    self.deathEffectSprite, 1 + n / 2), 255 - n * 51).image for n in range(5)],
                delay=4
            ))

            self.target.points += 10000
            drops = np.random.choice(
                self.drop[0], np.random.randint(1, 4), self.drop[1])
            drop_item = None
            for drop in drops:
                if drop == "power_large":
                    drop_item = PowerItem(
                        self.position + Vector2.random_int(-75, 75, -50, 0), True)
                elif drop == "power_small":
                    drop_item = PowerItem(
                        self.position + Vector2.random_int(-75, 75, -50, 0), False)
                elif drop == "points":
                    drop_item = PointItem(
                        self.position + Vector2.random_int(-75, 75, -50, 0))
                elif drop == "full_power":
                    drop_item = FullPowerItem(
                        self.position + Vector2.random_int(-75, 75, -50, 0))
                elif drop == "1up":
                    drop_item = OneUpItem(
                        self.position + Vector2.random_int(-75, 75, -50, 0))

                if drop_item is not None:
                    self.scene.items.append(drop_item)

        if self in self.scene.enemies:
            self.scene.enemies.remove(self)
        del self
