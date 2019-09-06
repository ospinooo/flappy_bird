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


GEN = 0

BG_IMG = pygame.transform.scale2x(pygame.image.load("./img/bg.png"))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))  # draw on the top left position

    for pipe in pipes:
        pipe.draw(win)

    score_text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    gen_text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))

    # It can go as higher as you want it will appear
    win.blit(score_text, (WIN_WIDTH - 10 -
                          score_text.get_width(), 10))  # top right
    win.blit(gen_text, (10, 10))  # top left
    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    """FItness function for the neat execution
    """
    global GEN
    GEN += 1

    # Each position is for each bird.
    nets = []  # Keep track of each nets
    ge = []
    birds = []

    # genomes have id and the object
    for _, g in genomes:
        # set a nn for the genome
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))  # All birds start at the same position
        g.fitness = 0  # Init fitness
        ge.append(g)

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

        pipe_ind = 0
        print(len(birds))
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                # if they have passed the pipe the ind will be 1, start focusing on the next pipe
                pipe_ind = 1
        elif len(birds) == 0:
            # If there is no birds left
            run = False
            break

        for x, bird in enumerate(birds):
            # Give fitness if its still alive
            bird.move()
            ge[x].fitness += 0.1

            # Neural Network.
            # height of the bird and how far it is from the pipes.
            output = nets[x].activate(
                (bird.y, abs(bird.y-pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    # if a bird hits a pipe it will have a lower fitness
                    ge[x].fitness -= 1
                    # Remove bird and genome
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

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
            for g in ge:
                # Any genome in the list is still alive so we increase the fitness.
                g.fitness += 5
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < -50:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if score > 50:
            break

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)  # 50 generations, call 50 times the function main
    print('\n Best genome \n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)  # path to the current dir
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
