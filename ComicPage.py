
import pygame
import random

from StarObject import StarObject
from IconRepository import IconRepository
from ShipClass import Stationary


class ComicPage ( StarObject ) :

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, game, page_name, x, y, size) :
        "x, y, size are screen coords"
        super().__init__(game, Stationary( None, size ), x, y )
        self.Z = 0
        self.filename = f'./comic/{page_name}.jpg'
        self.zoom = 0.001
        self.size = size
        page = pygame.image.load(self.filename)
        self.icon = IconRepository.resize(page, size)
        self.texts = []
        self.stop_requested = False

    def ticktack(self) :
        if self.stop_requested :
            self.zoom = self.game.approach_value(self.zoom, 0, 10)
        else :
            self.zoom = self.game.approach_value(self.zoom, 1, 30)

    def paint_bubble(self, win, text, x, y) :

        # Split the text into lines
        lines = text.splitlines()

        font = self.game.get_font()

        # Calculate the width and height of the text
        text_width = max(font.size(line)[0] for line in lines)
        text_height = sum(font.size(line)[1] for line in lines)

        # Draw the bubble
        bubble_rect = pygame.Rect(x, y, text_width, text_height)
        bubble_rect.inflate_ip(20,20)
        # pygame.draw.ellipse(win, ComicPage.BLACK, bubble_rect)
        # pygame.draw.ellipse(win, ComicPage.WHITE, bubble_rect, 2)
        pygame.draw.rect(win, ComicPage.BLACK, bubble_rect)
        pygame.draw.rect(win, ComicPage.WHITE, bubble_rect, 2)


        # Initial y coordinate
        for line in lines:
            # Render the line
            text_surface = font.render(line, True, ComicPage.WHITE)
            
            # Get the rectangle of the text surface and set its top left corner to your desired position
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y)  # Replace with your desired coordinates
            
            # Draw the text to the screen
            win.blit(text_surface, text_rect)
            
            # Update the y coordinate for the next line
            y += text_surface.get_height()

    def repaint(self, win):
        # Scale the icon
        scale_x, scale_y = self.icon.get_size()
        scale_x = int(scale_x * self.zoom)
        scale_y = int(scale_y * self.zoom)
        scaled_icon = pygame.transform.scale(self.icon, (scale_x, scale_y))

        # Create a new surface with a white border
        border_size = 5
        with_border_size = (scale_x + 2 * border_size, scale_y + 2 * border_size)
        bordered_icon = pygame.Surface(with_border_size, pygame.SRCALPHA)
        bordered_icon.fill((255, 255, 255))  # Fill with white color
        bordered_icon.blit(scaled_icon, (border_size, border_size))  # Blit the scaled icon at the border offset

        # Get the rect and blit the image with the border
        new_rect = bordered_icon.get_rect(center=(self.x, self.y))

        win.blit(bordered_icon, new_rect.topleft)

        if not self.stop_requested :
            for text, x, y in self.texts :
                self.paint_bubble(win, text, x, y )

    def add_text( self, text, x, y ) :
        self.texts.append( (text, x, y) )

    def on_stop_request(self) :
        self.stop_requested = True


