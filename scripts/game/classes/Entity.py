import pygame
from typing import Union

from scripts.framework.math.Vector2 import Vector2
from scripts.framework.ui.SpriteSheet import SpriteSheet


class Entity:
    def __init__(self):
        self.position: Vector2
        self.spritesheet: Union[SpriteSheet, list[pygame.sprite.Sprite]]
        self.name: str

        self.currentSprite = 0
        self.changeSpriteTimer = 0

        self.sprite = pygame.sprite.Sprite()

    def update(self) -> None:
        pass

    def nextSprite(self, delay: int) -> None:
        if self.changeSpriteTimer >= delay:
            self.currentSprite = (self.currentSprite +
                                  1) % len(self.spritesheet)
            self.changeSpriteTimer = 0

    def getSprite(self) -> pygame.sprite.Sprite:
        self.sprite.image = self.spritesheet[self.currentSprite]

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = self.position.to_tuple()

        return self.sprite
