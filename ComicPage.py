
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

    def paint_bubble_sq(self, win, text, x, y) :
        (lines,bubble_rect) = self.prepare_lines(text, x, y)
        bubble_rect.inflate_ip(20,20)
        pygame.draw.rect(win, ComicPage.BLACK, bubble_rect)
        pygame.draw.rect(win, ComicPage.WHITE, bubble_rect, 2)
        self.render_lines(win, bubble_rect.left + 10, bubble_rect.top + 10, lines)

    def prepare_lines(self, text, x, y) :
        lines = text.splitlines()
        font = self.game.get_font()

        # Calculate the width and height of the text
        text_width = max(font.size(line)[0] for line in lines)
        text_height = sum(font.size(line)[1] for line in lines)

        # Draw the bubble
        bubble_rect = pygame.Rect(x - text_width // 2, y - text_height // 2, text_width, text_height)
        return (lines, bubble_rect)

    def render_lines(self, win, x, y, lines) :
        font = self.game.get_font()
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

    def draw_rounded_rect(self, win, rect, color, radius):
        """Draw a rectangle with rounded corners"""
        pygame.draw.rect(win, color, rect.inflate(-2*radius, 0))
        pygame.draw.rect(win, color, rect.inflate(0, -2*radius))
        rect = rect.inflate(-2*radius, -2*radius)
        pygame.draw.circle(win, color, rect.topleft, radius)
        pygame.draw.circle(win, color, rect.topright, radius)
        pygame.draw.circle(win, color, rect.bottomleft, radius)
        pygame.draw.circle(win, color, rect.bottomright, radius)

    def draw_tail(self, win, from_xy, to_xy, color1, color2 ):
        """Draw a triangle for the tail of the speech bubble"""
        ANGLE = 2
        p_from = pygame.math.Vector2(*from_xy)
        p_to = pygame.math.Vector2(*to_xy)
        distance = p_from.distance_to(p_to)
        vector = p_to - p_from
        # Calculate point3 by adding the rotated vector to point1
        p1 = p_from + vector.rotate(-ANGLE)
        p2 = p_from + vector.rotate(ANGLE)
        pygame.draw.polygon(win, color2, [ p_from, p1, p2 ])
        pygame.draw.line(win, color1, p_from, p1, 3 )
        pygame.draw.line(win, color1, p_from, p2, 3 )

    def draw_speech_bubble(self, win, text, from_xy, to_xy ) :
        # rect, color, radius, tail_tip, tail_width, tail_height):
        """Draw the speech bubble"""
        RADIUS = 15
        (lines,bubble_rect) = self.prepare_lines(text, *to_xy)
        bubble_rect.inflate_ip(30,30)
        self.draw_rounded_rect(win, bubble_rect, ComicPage.WHITE, RADIUS+2)
        self.draw_tail(win, from_xy, to_xy, ComicPage.WHITE, ComicPage.BLACK)
        bubble_rect.inflate_ip(-4,-4)
        self.draw_rounded_rect(win, bubble_rect, ComicPage.BLACK, RADIUS)
        self.render_lines(win, bubble_rect.left + 15, bubble_rect.top + 15, lines)

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
            for text, sx, sy, x, y in self.texts :
                if sx==None and sy==None :
                    self.paint_bubble_sq(win, text, x, y )
                else :
                    self.draw_speech_bubble(win, text, (sx, sy), (x, y))

    def add_text( self, text, to_xy ) :
        self.texts.append( (text, None, None, *to_xy) )

    def add_speech( self, text, to_xy, from_xy ) :
        self.texts.append( (text, *from_xy, *to_xy))
        print(f'texts now: {self.texts}')

    def on_stop_request(self) :
        self.stop_requested = True


