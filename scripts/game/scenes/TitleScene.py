import pygame.image
import time
from pygame.locals import *

from os.path import join as path_join

from scripts.framework.environment import *
from scripts.framework.math.Vector2 import Vector2
from scripts.framework.ui.SelectButtonMatrix import SelectButtonMatrix
from scripts.framework.ui.Scene import Scene, renderFps

from scripts.game.scenes.GameScene import GameScene


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        musicModule.playMusic("TitleScreen.wav")

        self.background = pygame.sprite.Sprite()
        self.background.rect = (0, 0, WIDTH, HEIGHT)
        self.background.image = pygame.image.load(
            path_join("assets", "sprites", "backgrounds",
                      "title_screen_wallpaper.jpg")
        ).convert_alpha()

        self.font = pygame.font.Font(
            path_join("assets", "fonts", "DFPPOPCorn-W12.ttf"), 45)

        self.matrix = [[["Start", self.switchToGame]], [["Quit", self.quit]]]
        self.ButtonMatrix = SelectButtonMatrix(
            Vector2(100, 100), self.matrix, self.font, (100, 100, 100), (255, 50, 40))

    @renderFps
    def render(self, screen, clock):
        background_group = pygame.sprite.RenderPlain()
        background_group.add(self.background)

        background_group.draw(screen)

        self.ButtonMatrix.draw(screen)

    def processInput(self, events):
        self.ButtonMatrix.handle_events(events)

        for evt in events:
            if evt.type == QUIT:
                pygame.quit()

    def switchToGame(self):
        self.switchToScene(GameScene("yuyuko"))

    def quit(self):
        musicModule.sounds[0](.1)
        time.sleep(.3)
        pygame.quit()
