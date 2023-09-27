import random
import numpy

from scripts.framework.math.Vector2 import Vector2

from scripts.game.classes.Bullet import Bullet
from scripts.game.classes.BulletData import BulletData
from scripts.game.classes.Enemy import Enemy
from scripts.game.classes.Player import Player


class AttackFunctions:
    deltaAngle = 0

    @staticmethod
    def ring(center: Vector2, numberOfBullets: int, bulletData: BulletData, speed: float, angularSpeed: float = 0,
             deltaAngle: float = 0):
        bullets = [
            Bullet(
                bulletData,
                center,
                (360 * n / numberOfBullets + deltaAngle) % 360,
                speed,
                angularSpeed
            )
            for n in range(numberOfBullets)
        ]

        return bullets

    @staticmethod
    def random(center: Vector2, numberOfBullets: int, bulletData: BulletData, speed: float,
               angularSpeed: float = 0):
        bullets = [
            Bullet(
                bulletData,
                center,
                random.randint(0, 360),
                speed,
                angularSpeed
            )
            for _ in range(numberOfBullets)
        ]

        return bullets

    @staticmethod
    def cone(center: Vector2, angle, numberOfBullets: int, bulletData: BulletData, speed: float, deltaAngle: int, angularSpeed=0, player: Player = None, enemy: Enemy = None):
        bullets = [
            Bullet(
                bulletData,
                center,
                (angle if angle != "player" else numpy.rad2deg(Vector2.angle_between(
                    enemy.position - player.position, Vector2.right())) + 90) + i * deltaAngle * 0.5,
                speed,
                angularSpeed
            )

            for i in range(-numberOfBullets + 1, numberOfBullets, 2)
        ]

        return bullets

    @staticmethod
    def wideCone(numberOfBullets: int, numberOfCones: int, bulletData: BulletData, angle: int, speed: float, deltaAngle: int,
                 startTime: float, delay: float, angularSpeed=0, player: Player = None, enemy: Enemy = None):
        center = Vector2.zero()

        attacks = [
            (
                AttackFunctions.cone,
                round(startTime + delay * n, 3),
                [center, angle, numberOfBullets, bulletData,
                    speed, deltaAngle, angularSpeed, player, enemy]
            )
            for n in range(numberOfCones)
        ]

        return attacks

    @staticmethod
    def wideRing(numberOfBullets: int, numberOfRings: int, bulletData: BulletData, speed: float,
                 startTime: float, delay: float, angularSpeed: float = 0, deltaAngle: float = 0, randomCenter=False):

        attacks = [
            (
                AttackFunctions.ring,
                round(startTime + delay * n, 3),
                [Vector2.zero() if not randomCenter else
                 Vector2.one().rotate(random.randint(0, 360)) * 25, numberOfBullets, bulletData, speed, angularSpeed, n * deltaAngle]
            )
            for n in range(numberOfRings)
        ]

        return attacks

    @staticmethod
    def longRandom(numberOfBullets: int, randomAmount: int, bulletData: BulletData, speed: float,
                   startTime: float, delay: float, angularSpeed: float = 0, randomCenter=False):
        attacks = [
            (
                AttackFunctions.random,
                round(startTime + delay * n, 3),
                [Vector2.zero() if not randomCenter else
                 Vector2.one().rotate(random.randint(0, 360)) * 25, numberOfBullets, bulletData, speed, angularSpeed]
            )
            for n in range(randomAmount)
        ]

        return attacks
