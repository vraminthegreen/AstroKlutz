
import pygame

from StarObject import StarObject
from ShipClass import ObjectClass



class Group( StarObject ) :

    def __init__(self, game, number) :
        super().__init__(game, ObjectClass(), 0, 0)
        self.visible = False
        self.focus_visible = True
        self.ships = []
        self.bounding_rect = pygame.Rect(0,0,0,0)
        self.number = number
        self.background_color = [0, 128, 128, 64]
        self.background_color2 = [0, 128, 128, 120]
        self.minimized_size = 32
        self.game.register_key_handler( str(number), self )
        self.select_animation = None

    def add_ship(self,ship) :
        self.ships.append(ship)
        if len(self.ships) == 1 :
            self.bounding_rect = ship.get_rect()
        else :
            self.bounding_rect.union_ip(ship.get_rect())
        self.visible = True
        (self.x,self.y) = self.bounding_rect.center
        self.size = max(self.bounding_rect.width, self.bounding_rect.height)

    def remove_ship(self,ship) :
        self.ships.remove(ship)
        if len(self.ships) == 0 :
            self.visible = False
            return
        self.update_bounding_rect()

    def update_bounding_rect(self) :
        self.bounding_rect = self.ships[0].get_rect()
        for aship in self.ships[1:] :
            self.bounding_rect.union_ip(aship)
        (self.x,self.y) = self.bounding_rect.center
        self.size = max(self.bounding_rect.width, self.bounding_rect.height)

    def get_rect(self) :
        return self.bounding_rect

    def ticktack(self) :
        if self.select_animation != None :
            self.select_animation -= 1
            if self.select_animation < 0 :
                self.select_animation = None

    def repaint(self, win):
        # Calculate group's position and size based on its number
        group_height = self.minimized_size + 10  # 10 for padding
        group_y = 10 + (self.number - 1) * group_height  # 10 for top margin
        group_width = len(self.ships) * self.minimized_size + 30  # 30 for padding and number

        bg = self.background_color
        if self.select_animation != None and ( ( self.select_animation // 3 ) % 2 == 0 ) :
            bg = self.background_color2

        # Draw semi-transparent background
        background_rect = pygame.Surface((group_width, group_height), pygame.SRCALPHA)
        background_rect.fill(bg)
        win.blit(background_rect, (10, group_y))  # 10 for left margin

        # Draw group number
        font = pygame.font.Font(None, self.minimized_size)  # Use default font
        number_surface = font.render(str(self.number), True, (50, 255, 200))
        win.blit(number_surface, (15, group_y + 10))  # 15 for left margin, 5 for top padding

        # Draw ship miniatures
        icon_x = 35
        for i, ship in enumerate(self.ships):
            icon = pygame.transform.scale(ship.icon, (ship.minimized_size, ship.minimized_size))
            rotated_icon = pygame.transform.rotate(icon, 90)  # Rotate icon by -90 degrees
            win.blit(rotated_icon, (icon_x, group_y + 5 + (self.minimized_size - ship.minimized_size)/2))  # 5 for top padding
            icon_x += ship.minimized_size + 5  # 30 for left margin and number

    def on_key_pressed( self, key ) :
        if key != str(self.number) :
            return
        self.game.set_focused( self )
        self.select_animation = 20

