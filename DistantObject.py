
import pygame

from StarObject import StarObject

class DistantObject ( StarObject ) :

    def repaint(self, win):

        ico = self.get_icon()
        if ico == None :
            return

        # Scale the icon
        scale_x, scale_y = ico.get_size()
        scale_x = int(scale_x * pow(self.game.zoom,0.2))
        scale_y = int(scale_y * pow(self.game.zoom,0.2))
        scaled_icon = pygame.transform.scale(ico, (scale_x, scale_y))

        new_rect = scaled_icon.get_rect( center = self.game.get_display_xy(self.x, self.y, self.layer) )
        win.blit(scaled_icon, new_rect.topleft)
