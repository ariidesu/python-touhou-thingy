from os.path import join as path_join
import numpy

from scripts.framework.environment import *
from scripts.framework.math.Collider import Collider
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.ui.Scene import Scene
from scripts.framework.ui.SpriteSheet import SpriteSheet

from scripts.game.classes.AttackFunctions import AttackFunctions
from scripts.game.classes.BulletData import BulletData, BulletDataPresets
from scripts.game.classes.Enemy import Enemy
from scripts.game.classes.Player import Player

gameZoneVector = Vector2(GAME_ZONE[0], GAME_ZONE[1])

class TimelineRunner:
    def __init__(self, scene: Scene, player: Player, levelData: any):
        self.linkedScene = scene
        self.linkedPlayer = player
        self.levelData = levelData
        self.passedTime = []
        self.enemies = []
        self.bulletsPool = []

    def onTime(self, currentTime: int):
        for i in self.levelData["timeline"]:
            if i in self.passedTime:
                continue

            timelineTime = float(i)
            if currentTime >= timelineTime:
                self.passedTime.append(i)
                
                currentTimelineData = self.levelData["timeline"][i]
                if currentTimelineData["action"] == "spawn":
                    print("spawn at", i)
                    usingEnemyData = None
                    if self.levelData["presets"] and currentTimelineData["enemy"] in self.levelData["presets"]:
                        usingEnemyData = self.levelData["presets"][currentTimelineData["enemy"]]
                    else:
                        print("no built in enemy")

                    if usingEnemyData is not None:
                        spritePath = path_join(*usingEnemyData["sprite"]["path"]) if "path" in usingEnemyData["sprite"] else path_join("assets", "sprites", "entities", usingEnemyData["sprite"]["spriteFile"])
                        enemySprite = SpriteSheet(spritePath).crop(usingEnemyData["sprite"]["size"]),
                        enemyHp = currentTimelineData["hp"] or 5
                        enemyPosition = gameZoneVector + Vector2(*currentTimelineData["position"])
                        enemySpeed = currentTimelineData["speed"]
                        enemyTrajectory = list(map(numpy.array, [currentTimelineData["position"]] + currentTimelineData["trajectory"]))
                        enemyDrop = (currentTimelineData["drop"]["list"], currentTimelineData["drop"]["list"])
                        clearBulletsOnDeath = currentTimelineData["clearOnDeath"]

                        enemy = Enemy(
                            spritesheet=enemySprite,
                            hp=enemyHp,
                            position=enemyPosition,
                            speed=enemySpeed,
                            trajectory=enemyTrajectory,
                            collider=Collider(usingEnemyData["collider"]["radius"], offset=usingEnemyData["collider"]["offset"]),
                            drop=enemyDrop,
                            clearBulletsOnDeath=clearBulletsOnDeath,
                            attackData=[],
                            bulletPool=self.bulletsPool,
                            scene=self.linkedScene
                        )

                        enemyAttackData = []
                        for attackData in currentTimelineData["attacks"]:
                            newBullets = None
                            if attackData["type"] == "wideRing":
                                newBullets = AttackFunctions.wideRing(
                                        numberOfBullets=attackData["bullets"],
                                        numberOfRings=attackData["rings"],
                                        bulletData=BulletData(BulletDataPresets[attackData["bulletType"]]["spritesheet"], BulletDataPresets[attackData["bulletType"]]["collider"], BulletDataPresets[attackData["bulletType"]]["animationSpeed"]),
                                        speed=attackData["speed"],
                                        angularSpeed=attackData["angularSpeed"],
                                        deltaAngle=attackData["angleIncremental"],
                                        startTime=attackData["startTime"],
                                        delay=attackData["delay"],
                                        randomCenter=attackData["randomCenter"]
                                    )
                                
                            elif attackData["type"] == "longRandom":
                                newBullets = AttackFunctions.longRandom(
                                        numberOfBullets=attackData["bullets"],
                                        randomAmount=attackData["randomAmount"],
                                        bulletData=BulletData(BulletDataPresets[attackData["bulletType"]]["spritesheet"], BulletDataPresets[attackData["bulletType"]]["collider"], BulletDataPresets[attackData["bulletType"]]["animationSpeed"]),
                                        speed=attackData["speed"],
                                        angularSpeed=attackData["angularSpeed"],
                                        startTime=attackData["startTime"],
                                        delay=attackData["delay"],
                                        randomCenter=attackData["randomCenter"]
                                    )
                            elif attackData["type"] == "wideCone":
                                newBullets = AttackFunctions.wideCone(
                                        numberOfBullets=attackData["bullets"],
                                        numberOfCones=attackData["cones"],
                                        bulletData=BulletData(BulletDataPresets[attackData["bulletType"]]["spritesheet"], BulletDataPresets[attackData["bulletType"]]["collider"], BulletDataPresets[attackData["bulletType"]]["animationSpeed"]),
                                        speed=attackData["speed"],
                                        angle=attackData["angle"],
                                        angularSpeed=attackData["angularSpeed"],
                                        deltaAngle=attackData["angleIncremental"],
                                        startTime=attackData["startTime"],
                                        delay=attackData["delay"],
                                        player=self.linkedPlayer,
                                        enemy=enemy
                                    )

                            if newBullets is not None:
                                enemyAttackData.extend(newBullets)

                        enemy.attackData = sorted(enemyAttackData, key=lambda x: x[1])
                        self.enemies.append(enemy)