#!/usr/bin/env python3
import pygame
import os
import math
import random

from Scenarios import BasicScenario, Scenario1

pygame.init()
pygame.font.init()
win = pygame.display.set_mode( (1280,720) )


# BasicScenario().start()

Scenario1(win).start()

pygame.quit()
