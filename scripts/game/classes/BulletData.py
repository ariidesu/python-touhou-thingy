from os.path import join as path_join

from scripts.framework.math.Collider import Collider
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.ui.SpriteSheet import SpriteSheet

BulletDataPresets = {
    "kunai": {
        "spritesheet": SpriteSheet(path_join("assets", "sprites", "projectiles", "kunai_0.png")).crop((16, 16)),
        "collider": Collider(4, Vector2(0, 0)),
        "animationSpeed": 0,
    }
}

class BulletData:
    def __init__(self, spritesheet: SpriteSheet, collider: Collider, animationSpeed: int = 0):
        self.spritesheet = spritesheet
        self.collider = collider
        self.animationSpeed = animationSpeed

    def __repr__(self):
        return f"BulletData({self.spritesheet}, {self.collider}, {self.animationSpeed})"
