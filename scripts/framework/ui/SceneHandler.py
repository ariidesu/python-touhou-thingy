import pygame

from scripts.framework.environment import *
from scripts.framework.ui.Scene import Scene


class SceneHandler:
    def __init__(self, screen: pygame.display, clock: pygame.time.Clock):
        self.currentScene = None
        self.screen = screen
        self.clock = clock

    def getScene(self) -> Scene:
        return self.currentScene

    def setScene(self, scene: Scene):
        self.currentScene = scene

    def update(self, deltaTime: float):
        if self.currentScene is not None:
            self.currentScene.processInput(pygame.event.get())
            self.currentScene.update(deltaTime)
            self.currentScene.render(self.screen, self.clock)

            self.currentScene = self.currentScene.next
