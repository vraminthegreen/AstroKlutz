import pygame
import os
import math

class Game:
    def __init__(self, input_handler):
        self.starships = []
        self.input_handler = input_handler
        self.win = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def add_object(self, starship):
        self.starships.append(starship)

    def remove_object(self, starship):
        self.starships.remove(starship)

    def game_loop(self):
        running = True
        while running:
            self.clock.tick(60)  # Limit the game loop to 60 frames per second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.win.fill((255, 255, 255))
            self.input_handler.handle_input()
            for starship in self.starships:
                starship.ticktack()
                starship.repaint(self.win)
            pygame.display.flip()

        pygame.quit()


