import pygame
from pygame.locals import *

from scripts.framework.enviroment import *
from scripts.framework.ui.SceneHandler import *
from scripts.game.scenes.TitleScene import TitleScene

def init():
    pygame.init()

    pygame.mixer.pre_init(48000, -16, 2, 4096)
    pygame.mixer.init()

def run():
    screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)
    clock = pygame.time.Clock()

    currentScene = TitleScene()
    deltaTime = 1 / FPS

    while currentScene is not None:
        updateScene(screen, clock, deltaTime)
        pygame.display.flip()
        deltaTime = clock.tick(FPS) / 1000