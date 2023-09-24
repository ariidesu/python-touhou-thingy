import pygame

from scripts.framework.enviroment import *

currentScene = None

def updateScene(screen: pygame.display, clock: pygame.time.Clock, deltaTime: float):
    if currentScene is not None:
        currentScene.processInput(pygame.event.get())
        currentScene.update(deltaTime)
        currentScene.render(screen, clock)

        currentScene = currentScene.next