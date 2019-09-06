import os
import pygame

BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join(os.path.join(
        os.path.dirname(__file__), "..", "img", "base.png"))))


class Base:

    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y

        # 2 images to show its moving
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # Move images same speed
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Put the image to the back when it is off the screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        # Both images
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
