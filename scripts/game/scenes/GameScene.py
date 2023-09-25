import numpy
import pygame
from pygame.locals import *
import json
from PIL import Image

from scripts.framework.environment import *
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.ui.Scene import Scene, renderFps
from scripts.framework.ui.SpriteSheet import SpriteSheet

from scripts.game.classes.AttackFunctions import AttackFunctions
from scripts.game.classes.BulletData import BulletData
from scripts.game.classes.Enemy import Enemy
from scripts.game.classes.Item import *
from scripts.game.classes.Player import Player


class GameScene(Scene):
    def __init__(self, level: str):
        super().__init__()
        self.GAME_ZONE = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))
        self.deltaTime = 0.001
        
        self.level = json.load(
            open(path_join("assets", "levels", f"{level}.json")))
        self.levelEnemies = sorted(
            self.level["enemies"], key=lambda enemy: enemy["time"])

        musicModule.playMusic(self.level["bgm"])

        self.background = Image.open(path_join(
            "assets", "sprites", "backgrounds", "background.png")).convert("RGBA")
        self.background.paste(Image.new("RGBA", (GAME_ZONE[2], GAME_ZONE[3]), (255, 255, 255, 0)),
                              (GAME_ZONE[0], GAME_ZONE[1]))
        self.bg = pygame.sprite.Sprite()
        self.bg.rect = Rect(0, 0, WIDTH, HEIGHT)
        self.bg.image = pygame.image.fromstring(self.background.tobytes(
        ), self.background.size, self.background.mode).convert_alpha()

        self.font = pygame.font.Font(
            path_join("assets", "fonts", "DFPPOPCorn-W12.ttf"), 36)

        self.player = Player(0, self, 4)

        self.enemyBullets = []
        self.items = []
        self.bulletCleaner = None

        self.effects = []

        self.bulletGroup = pygame.sprite.RenderPlain()
        self.itemGroup = pygame.sprite.RenderPlain()
        self.hudGroup = pygame.sprite.RenderPlain()
        self.entityGroup = pygame.sprite.RenderPlain()
        self.effectGroup = pygame.sprite.RenderPlain()

        self.time = 0
        self.enemyCount = 0

        self.enemies = []

    def processInput(self, events):
        for evt in events:
            if evt.type == QUIT:
                pygame.quit()

        moveDirection = Vector2.zero()

        if pygame.key.get_pressed()[pygame.K_UP]:
            moveDirection += Vector2.up()
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            moveDirection += Vector2.down()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            moveDirection += Vector2.left()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            moveDirection += Vector2.right()

        if pygame.key.get_pressed()[pygame.K_z]:
            self.player.shoot()

        self.player.move(moveDirection)

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.player.slow = True
        else:
            self.player.slow = False

    def update(self, deltaTime):
        self.deltaTime = deltaTime
        self.time += deltaTime

        if self.time >= self.level["length"]:
            self.player.switchToTitle()

        if self.levelEnemies and self.enemyCount < len(self.levelEnemies):
            if self.time >= self.levelEnemies[self.enemyCount]["time"]:
                enemyData = self.levelEnemies[self.enemyCount]
                enemy = Enemy(
                    position=Vector2(
                        GAME_ZONE[0], GAME_ZONE[1]) + Vector2(*enemyData["startPosition"]),
                    trajectory=list(
                        map(numpy.array, [enemyData["startPosition"]] + enemyData["trajectory"])),
                    speed=enemyData["speed"],
                    spritesheet=SpriteSheet(
                        path_join(*enemyData["sprite"]["path"])).crop(enemyData["sprite"]["size"]),
                    collider=Collider(enemyData["collider"]["radius"], offset=Vector2(
                        *enemyData["collider"]["offset"])),
                    hp=enemyData["hp"],
                    attackData=[(*attack[:3], (path_join(*attack[3][0]), attack[3][1], attack[3][2], attack[3]
                                 [3], Vector2(*attack[3][4])), *attack[4:]) for attack in enemyData["attacks"]],
                    drop=(enemyData["drop"]["list"],
                          enemyData["drop"]["list"]),
                    clearBulletsOnDeath=enemyData["clearOnDeath"],
                    bulletPool=self.enemyBullets,
                    scene=self
                )

                attackData = []
                for i in range(len(enemy.attackData)):
                    if enemy.attackData[i][0] == "wideRing":
                        _, bul_num, ring_num, bul_data, spd, s_time, delay, a_speed, d_angle, rand_cnt = \
                            enemy.attackData[i]
                        attackData.extend(
                            AttackFunctions.wideRing
                            (
                                numberOfBullets=bul_num,
                                numberOfRings=ring_num,
                                bulletData=BulletData(
                                    SpriteSheet(bul_data[0]).crop(
                                        (bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                speed=spd,
                                startTime=s_time,
                                delay=delay,
                                angularSpeed=a_speed,
                                deltaAngle=d_angle,
                                randomCenter=rand_cnt
                            )
                        )
                    elif enemy.attackData[i][0] == "longRandom":
                        _, bul_num, rand_num, bul_data, spd, s_time, delay, a_speed, rand_cnt = \
                            enemy.attackData[i]
                        attackData.extend(
                            AttackFunctions.longRandom
                            (
                                numberOfBullets=bul_num,
                                randomAmount=rand_num,
                                bulletData=BulletData(
                                    SpriteSheet(bul_data[0]).crop(
                                        (bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                speed=spd,
                                startTime=s_time,
                                delay=delay,
                                angularSpeed=a_speed,
                                randomCenter=rand_cnt
                            )
                        )
                    elif enemy.attackData[i][0] == "wideCone":
                        _, bul_num, cone_num, bul_data, angle, spd, d_angle, s_time, delay, a_speed = enemy.attackData[
                            i]
                        attackData.extend(
                            AttackFunctions.wideCone(
                                numberOfBullets=bul_num,
                                numberOfCones=cone_num,
                                bulletData=BulletData(
                                    SpriteSheet(bul_data[0]).crop(
                                        (bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                angle=angle,
                                speed=spd,
                                deltaAngle=d_angle,
                                startTime=s_time,
                                delay=delay,
                                angularSpeed=a_speed,
                                player=self.player,
                                enemy=enemy
                            )
                        )

                enemy.attackData = sorted(attackData, key=lambda x: x[1])

                self.enemies.append(enemy)
                self.enemyCount += 1

        for enemy in self.enemies:
            enemy.update()
            enemy.move()

        for bullet in self.player.bullets:
            on_screen = bullet.move(deltaTime)
            if not on_screen:
                self.player.bullets.remove(bullet)
                del bullet

        for item in self.items:
            on_screen = item.move(deltaTime, self.player)
            if not on_screen:
                self.items.remove(item)
                del item

        for effect in self.effects:
            ended = not effect.update(deltaTime)
            if ended:
                self.effects.remove(effect)
                del effect

        if self.bulletCleaner:
            self.bulletCleaner.update(self.enemyBullets, self, deltaTime)
            if self.bulletCleaner.kill:
                del self.bulletCleaner
                self.bulletCleaner = None

        for bullet in self.enemyBullets:
            on_screen = bullet.move(deltaTime)
            if not on_screen:
                self.enemyBullets.remove(bullet)
                del bullet

        self.player.update()

    @renderFps
    def render(self, screen, clock):
        screen.fill((0, 0, 0), rect=GAME_ZONE)

        for bullet in self.player.bullets:
            self.bulletGroup.add(bullet.getSprite())

        for bullet in self.enemyBullets:
            self.bulletGroup.add(bullet.getSprite())

        for item in self.items:
            self.itemGroup.add(item.getSprite())

        for effect in self.effects:
            self.effectGroup.add(effect.getSprite())

        self.hudGroup.add(self.bg)

        scoreLabel = self.font.render(
            f"Score:    {format(self.player.points, '09d')}", True, (255, 255, 255)).convert_alpha()

        powerLabel = self.font.render(f"Power:    {format(round(self.player.power, 2), '.2f')} / 4.00", True,
                                      (255, 255, 255)).convert_alpha()

        hpLabel = self.font.render(
            f"Player:   {'★' * self.player.hp}", True, (255, 255, 255)).convert_alpha()

        player_sprite = self.player.getSprite()
        if self.player.slow or (self.player.reviving and self.player.invincibilityTimer % 40 > 30):
            player_sprite.image.set_alpha(150)

        self.entityGroup.add(player_sprite)

        for enemy in self.enemies:
            self.entityGroup.add(enemy.getSprite())

        self.entityGroup.draw(screen)
        self.itemGroup.draw(screen)
        self.bulletGroup.draw(screen)
        self.effectGroup.draw(screen)

        if self.bulletCleaner:
            screen.blit(self.bulletCleaner.getSprite(
            ), (self.bulletCleaner.collider.position - self.bulletCleaner.collider.radius).to_tuple())

        if self.player.slow:
            playerHitboxSprite = self.player.getHitboxSprite()
            screen.blit(playerHitboxSprite, (self.player.position -
                        (Vector2(*playerHitboxSprite.get_size())) // 2).to_tuple())

        self.hudGroup.draw(screen)

        screen.blit(scoreLabel, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 210))
        screen.blit(hpLabel, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 210 + 55))
        screen.blit(
            powerLabel, (GAME_ZONE[0] + GAME_ZONE[2] + 50, 210 + 55 + 55))

        self.effectGroup.empty()
        self.entityGroup.empty()
        self.itemGroup.empty()
        self.bulletGroup.empty()
        self.bulletGroup.empty()
        self.hudGroup.empty()
