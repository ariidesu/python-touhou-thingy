import numpy as np
import pygame.surface

from scripts.framework.enviroment import music_module
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
                 sprite_sheet: SpriteSheet,
                 collider: Collider,
                 hp: int,
                 attack_data: [(callable, float), ...],
                 drop,
                 clear_bullets_on_death,
                 bullet_pool,
                 scene):

        super().__init__()
        self.start_position: Vector2 = position
        self.position: Vector2 = position
        self.trajectory = trajectory
        self.t = 0

        self.max_hp: int = hp
        self.current_hp: int = self.max_hp

        self.attack_data: [(callable, float), ...] = attack_data
        self.attack_count = 0

        self.sprite_sheet = sprite_sheet
        self.current_sprite = 0
        self.change_sprite_timer = 10

        self.deathEffectSprite = pygame.sprite.Sprite()
        self.deathEffectSprite.image = pygame.image.load(path_join("assets", "sprites", "effects", "fairy_death_0.png")).convert_alpha()
        self.deathEffectSprite.rect = self.deathEffectSprite.image.get_rect()

        self.bulletSpawnSprite = pygame.sprite.Sprite()
        self.bulletSpawnSprite.image = pygame.image.load(path_join("assets", "sprites", "effects", "bullet_spawn_effect.png")).convert_alpha()
        self.bulletSpawnSprite.rect = self.bulletSpawnSprite.image.get_rect()

        self.clear_bullets_on_death = clear_bullets_on_death

        self.bullets: list = bullet_pool

        self.collider: Collider = collider
        self.drop = drop

        self.scene = scene
        self.target = scene.player

        self.speed = speed

    def move(self) -> None:
        self.collider.position = self.position + self.collider.offset

        delta_time = self.scene.delta_time

        self.position = Vector2(coords=BSpline.curve(self.trajectory, self.t)) + Vector2(GAME_ZONE[0], GAME_ZONE[1])
        self.t += self.speed * delta_time
        if self.t > len(self.trajectory) - 1:
            self.death()

    def update(self) -> None:
        self.change_sprite_timer += 1 * 60 * self.scene.delta_time

        if self.attack_data and self.attack_count < len(self.attack_data):
            if self.t >= self.attack_data[self.attack_count][1]:
                music_module.sounds[3](.1)
                bullets = self.attack_data[self.attack_count][0](*self.attack_data[self.attack_count][2])

                for bullet in bullets:
                    bullet.position += self.position

                if len(self.bullets) > 0:
                    self.scene.effects.append(Effect(
                        position = bullets[0].position,
                        sprite_sheet = [setAlphaSprite(scaleSprite(self.bulletSpawnSprite, 3 - n / 2), 50 + n * 41).image for n in range(5)],
                        delay = 4
                    ))

                self.bullets.extend(bullets)
                self.attack_count += 1

        self.next_sprite(4)

        for bullet in self.target.bullets:
            if self.collider.check_collision(bullet.collider):
                self.target.points += 100
                self.get_damage(bullet.damage)
                self.target.bullets.remove(bullet)
                del bullet

    def get_damage(self, damage: int) -> None:
        music_module.sounds[2](.2)
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.death()

    def death(self):
        if self.current_hp <= 0:
            music_module.sounds[23](.15)

            if self.clear_bullets_on_death:
                self.scene.bullet_cleaner = BulletCleaner(self.position, give_points=True, show_sprite=False, increase_speed=2000)

            self.scene.effects.append(Effect(
                position=self.position,
                sprite_sheet=[setAlphaSprite(scaleSprite(self.deathEffectSprite, 1 + n / 2), 255 - n * 51).image for n in range(5)],
                delay=4
            ))

            self.target.points += 10000
            drops = np.random.choice(self.drop[0], np.random.randint(1, 4), self.drop[1])
            drop_item = None
            for drop in drops:
                if drop == "power_large":
                    drop_item = PowerItem(self.position + Vector2.random_int(-75, 75, -50, 0), True)
                elif drop == "power_small":
                    drop_item = PowerItem(self.position + Vector2.random_int(-75, 75, -50, 0), False)
                elif drop == "points":
                    drop_item = PointItem(self.position + Vector2.random_int(-75, 75, -50, 0))
                elif drop == "full_power":
                    drop_item = FullPowerItem(self.position + Vector2.random_int(-75, 75, -50, 0))
                elif drop == "1up":
                    drop_item = OneUpItem(self.position + Vector2.random_int(-75, 75, -50, 0))

                if drop_item is not None:
                    self.scene.items.append(drop_item)

        if self in self.scene.enemies:
            self.scene.enemies.remove(self)
        del self