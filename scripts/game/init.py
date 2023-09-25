import pygame
from pygame.locals import *

from scripts.framework.environment import *
from scripts.framework.ui.SceneHandler import SceneHandler


def run():
    pygame.display.set_caption("touhou python gamin (by cutymeo / shiinazzz)")
    screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)
    clock = pygame.time.Clock()
    sceneHandler = SceneHandler(screen, clock)

    from scripts.game.scenes.TitleScene import TitleScene

    sceneHandler.setScene(TitleScene())
    deltaTime = 1 / FPS

    while sceneHandler.getScene() is not None:
        sceneHandler.update(deltaTime)
        pygame.display.flip()
        deltaTime = clock.tick(FPS) / 1000
