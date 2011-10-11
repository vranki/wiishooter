import pygame

class Ak47:
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

    def close(self):
        pass
