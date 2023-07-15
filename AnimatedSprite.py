import pygame

class AnimatedSprite :

    def __init__(self, filename, columns, rows, size, overlay, frames=None):
        sprite_sheet = pygame.image.load("./assets/" + filename).convert_alpha()

        self.frames = []
        self.size = size
        self.frame_width = sprite_sheet.get_width() // columns
        self.frame_height = sprite_sheet.get_height() // rows

        for y in range(rows):
            for x in range(columns):
                frame = sprite_sheet.subsurface(pygame.Rect(x * self.frame_width, y * self.frame_height, self.frame_width, self.frame_height))
                frame = pygame.transform.smoothscale(frame, (size, size * frame.get_height() // frame.get_width()))
                self.frames.append(frame)

        if frames is not None and frames < len(self.frames):
            self.frames = self.frames[:frames]

        self.overlay = overlay

    def get_frame(self, frame_number):
        if frame_number < 0 or frame_number >= len(self.frames):
            return None
        else:
            return self.frames[frame_number]

    def get_overlay(self) :
        return self.overlay
