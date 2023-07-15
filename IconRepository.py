
import pygame

from collections import defaultdict


class IconRepository:

    repo = {}

    @staticmethod
    def _load_icon( key ) :
        (name, team, size) = key
        if team == None :
            filename = f'./assets/{name}.png'
        else :
            filename = f'./assets/{name}{team.get_filename_sufix()}.png'
        icon = pygame.image.load(filename)

        if size != None :
            orig_width, orig_height = icon.get_size()

            # Determine the aspect ratio
            aspect_ratio = orig_width / orig_height

            # Calculate new dimensions
            if aspect_ratio >= 1:  # Width is greater than height
                new_width = size
                new_height = int(size / aspect_ratio)
            else:  # Height is greater than width
                new_height = size
                new_width = int(size * aspect_ratio)

            # Resize the image with anti-aliasing
            icon = pygame.transform.smoothscale(icon, (new_width, new_height))
        icon = icon.convert_alpha()
        return icon

    @staticmethod
    def get_icon(name, size, team=None):
        key = (name, team, size)
        ico = IconRepository.repo.get( key )
        if ico == None :
            ico = IconRepository._load_icon( key )
            IconRepository.repo[ key ] = ico
        return ico

