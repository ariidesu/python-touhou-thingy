import pygame

from scripts.framework.math.Vector2 import Vector2


class Effect:
    def __init__(self, position: Vector2, spritesheet: [pygame.Surface, ...], delay: float):
        self.position: Vector2 = position

        self.spritesheet = spritesheet
        self.currentSprite = 0
        self.sprite_timer = 0

        self.delay = delay

    def update(self, deltaTime) -> bool:
        self.sprite_timer += deltaTime * 60 * 2
        if self.sprite_timer >= self.delay:
            self.currentSprite += 1

            self.sprite_timer = 0

            if self.currentSprite >= len(self.spritesheet):
                return False

        return True

    def getSprite(self) -> pygame.sprite.Sprite:
        sprite = pygame.sprite.Sprite()

        sprite.image = self.spritesheet[self.currentSprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite
