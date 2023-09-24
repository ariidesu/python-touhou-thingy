import pygame

def textButtonSprite(text: str, font: pygame.font.Font, default_color, selected_color) -> list[pygame.Surface]:
    return [
        font.render(text, True, default_color).convert_alpha(),
        font.render(text, True, selected_color).convert_alpha(),
    ]


def scaleSprite(sprite: pygame.sprite.Sprite, scale: float = 1) -> pygame.sprite.Sprite:
    new_sprite = pygame.sprite.Sprite()
    new_sprite.image = pygame.transform.scale(sprite.image,
                                              (sprite.rect.w * scale, sprite.rect.h * scale)).convert_alpha()
    new_sprite.rect = sprite.image.get_rect()
    return new_sprite


def setAlphaSprite(sprite: pygame.sprite.Sprite, alpha: int) -> pygame.sprite.Sprite:
    sprite.image.set_alpha(alpha)
    return sprite