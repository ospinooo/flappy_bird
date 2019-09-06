import pygame
import os

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join(os.path.join(os.path.dirname(__file__), "..", "img", "bird1.png")))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join(os.path.join(os.path.dirname(__file__), "..", "img", "bird2.png")))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join(os.path.join(os.path.dirname(__file__), "..", "img", "bird3.png"))))
]


class Bird:
    # Constants of the class
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # tail up and down
    ROT_VEL = 20  # each frame
    ANIMATION_TIME = 5  # how fast or slow the bird is flying

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0  # Seconds
        self.vel = 0  # Velocity
        self.height = self.y
        self.img_count = 0  # image we show
        self.img = self.IMGS[0]

    def jump(self):
        # Bird Fly up
        self.vel = -10.5  # Going upwards, 0,0 in the top left.
        self.tick_count = 0
        self.height = self.y  # Where it started jumping from

    def move(self):
        self.tick_count += 1
        # How many pixels to move

        # Physics how much we are moving up or down. (tick_count is the seconds)
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:  # Maximum velocity going down
            d = 16

        if d < 0:  # Jump a bit higher
            d -= 2

        self.y = self.y + d  # Actually Moving

        if d < 0 or self.y < self.height + 50:
            # moving upwards
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION  # set the rotation to the maximum if its not
        else:
            if self.tilt < -90:
                self.tilt -= self.ROT_VEL  # going down

    def draw(self, win):
        self.img_count += 1  # Keep track frames

        # Checking which image to show based on the ANIMATION_TIME
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)  # Two dimensional
