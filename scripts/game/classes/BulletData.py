from scripts.framework.math.Collider import Collider
from scripts.framework.ui.SpriteSheet import SpriteSheet


class BulletData:
    def __init__(self, spritesheet: SpriteSheet, collider: Collider, animationSpeed: int = 0):
        self.spritesheet = spritesheet
        self.collider = collider
        self.animationSpeed = animationSpeed

    def __repr__(self):
        return f"BulletData({self.spritesheet}, {self.collider}, {self.animationSpeed})"
