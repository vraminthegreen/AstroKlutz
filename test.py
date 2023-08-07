#!/usr/bin/env python3

import pygame
import math

def draw_rounded_rect(surface, rect, color, radius):
    """Draw a rectangle with rounded corners"""
    pygame.draw.rect(surface, color, rect.inflate(-2*radius, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -2*radius))
    rect = rect.inflate(-2*radius, -2*radius)
    pygame.draw.circle(surface, color, rect.topleft, radius)
    pygame.draw.circle(surface, color, rect.topright, radius)
    pygame.draw.circle(surface, color, rect.bottomleft, radius)
    pygame.draw.circle(surface, color, rect.bottomright, radius)

def draw_tail(surface, from_xy, to_xy, color1, color2 ):
    """Draw a triangle for the tail of the speech bubble"""
    ANGLE = 2
    p_from = pygame.math.Vector2(*from_xy)
    p_to = pygame.math.Vector2(*to_xy)
    distance = p_from.distance_to(p_to)
    vector = p_to - p_from
    # Calculate point3 by adding the rotated vector to point1
    p1 = p_from + vector.rotate(-ANGLE)
    p2 = p_from + vector.rotate(ANGLE)
    pygame.draw.polygon(surface, color2, [ p_from, p1, p2 ])
    pygame.draw.line(surface, color1, p_from, p1, 3 )
    pygame.draw.line(surface, color1, p_from, p2, 3 )
    # pygame.draw.polygon(surface, color2, [ pb, pb1, pb2 ])

def draw_speech_bubble(surface, text, from_xy, to_xy ) :
    # rect, color, radius, tail_tip, tail_width, tail_height):
    """Draw the speech bubble"""
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RADIUS = 15

    # font = self.game.get_font()
    font = pygame.font.Font('assets/Komika-Display/Komika_display.ttf', 18)

    lines = text.splitlines()

    # Calculate the width and height of the text
    text_width = max(font.size(line)[0] for line in lines)
    text_height = sum(font.size(line)[1] for line in lines)


    # Draw the bubble
    bubble_rect = pygame.Rect(0,0, text_width, text_height)
    bubble_rect.center = to_xy
    bubble_rect.inflate_ip(30,30)

    draw_rounded_rect(surface, bubble_rect, WHITE, RADIUS+2)
    draw_tail(surface, from_xy, to_xy, WHITE, BLACK)
    bubble_rect.inflate_ip(-4,-4)
    draw_rounded_rect(surface, bubble_rect, BLACK, RADIUS)

    x = to_xy[0] - text_width/2
    y = to_xy[1] - text_height/2
    # Initial y coordinate
    for line in lines:
        # Render the line
        text_surface = font.render(line, True, WHITE)
        
        # Get the rectangle of the text surface and set its top left corner to your desired position
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)  # Replace with your desired coordinates
        
        # Draw the text to the screen
        surface.blit(text_surface, text_rect)
        
        # Update the y coordinate for the next line
        y += text_surface.get_height()


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        # draw_speech_bubble(screen, pygame.Rect(50, 50, 200, 100), (255, 255, 255), 20, (150, 200), 20, 50)
        draw_speech_bubble(
            screen, 
            "TESTOWY TEKST\nKOMICZNY ALBO NIE\nALE ROZCIĄGAJĄCY SIĘ AŻ NA TRZY LINIJKI", 
            (100,400), (400,200))
            # npygame.Rect(50, 50, 200, 100), (255, 255, 255), 20, (150, 200), 20, 50)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

