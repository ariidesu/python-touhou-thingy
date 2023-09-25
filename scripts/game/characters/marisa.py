from os.path import join as path_join

from scripts.framework.math.Collider import Collider
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.ui.SpriteSheet import SpriteSheet

from scripts.game.classes.BulletData import BulletData
from scripts.game.classes.PlayerBullet import PlayerBullet

speed = 370
spritesheet = SpriteSheet(path_join(
    "assets", "sprites", "entities", "marisa_forward.png")).crop((25, 50))
bulletSpritesheet = SpriteSheet(path_join(
    "assets", "sprites", "projectiles", "marisa_bullet.png")).crop((32, 32))


def attack(fire_point: Vector2, power: int):
    bullets = []

    power_levels = [0, 1, 2, 3]
    deltaAngle = 10

    current_power = power_levels[int(
        (len(power_levels) - 1) * power * 20 / 100)]

    bulletData = BulletData(
        bulletSpritesheet, Collider(5, offset=Vector2.up() * 10))

    for i in range(-current_power, current_power + 1):
        i /= 2
        bullet_1 = PlayerBullet(
            bulletData, fire_point - Vector2(6, 0), deltaAngle * i, 900, damage=1)
        bullet_2 = PlayerBullet(
            bulletData, fire_point + Vector2(6, 0), deltaAngle * i, 900, damage=1)
        bullets.append(bullet_1)
        bullets.append(bullet_2)

    return bullets
