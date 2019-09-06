import os
import time
import random
import neat
import pygame

from flappy_bird.pipe import Pipe
from flappy_bird.bird import Bird
from flappy_bird.base import Base
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BG_IMG = pygame.transform.scale2x(pygame.image.load("./img/bg.png"))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))  # draw on the top left position

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    # It can go as higher as you want it will appear
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)

    pygame.display.update()


def main():
    # Run main loop of the game.
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()  # Doesn't depend on the computer

    score = 0
    run = True
    while run:
        clock.tick(30)  # At most 30 ticks every second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                return None

            if not pipe.passed and pipe.x < bird.x:
                # As soon as the bird passed the pipe
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                # It is out of the screen
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < -50:
            return

        base.move()
        draw_window(win, bird, pipes, base, score)


while True:
    main()
