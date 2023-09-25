# Initialize (top-level)
from scripts.game.init import *
import pygame
pygame.init()
pygame.mixer.pre_init(48000, -16, 2, 4096)
pygame.mixer.init()

# Main app
run()
