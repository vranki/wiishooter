import pygame
from ak47 import Ak47

class Ak47Mouse(Ak47):
    def __init__(self):
        pass

    def load_calibration(self, file_name):
        pass

    def get_pos(self):
        pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        return pos, buttons[0]

    def fire(self, trig):
        pass

    def reload_ak(self):
        buttons = pygame.mouse.get_pressed()
        return buttons[2] 

    def close(self):
        pass
