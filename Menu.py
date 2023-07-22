
import pygame
import math

from Game import Game
from StarObject import StarObject
from ShipClass import Stationary
from AnimatedSprite import AnimatedSprite

#################################################

class MenuItem :

    ICON_SIZE = 32

    def __init__( self, icon, not_selected, selected, label, action ) :
        """
        icon: AnimatedSprite
        not_selected: number of frame for not selected
        selected: number of frame for selected
        """
        self.icon = icon
        self.label = label
        self.action = action
        self.selected = selected
        self.not_selected = not_selected

    def get_frame( self, focused ) :
        frameno = self.selected if focused else self.not_selected
        return self.icon.get_frame( frameno )

    def set_pos(self, x, y) :
        self.x = x
        self.y = y

    def get_collision_rect(self) :
        rect = pygame.Rect(0, 0, MenuItem.ICON_SIZE*0.7, MenuItem.ICON_SIZE*0.7)
        rect.center = (self.x, self.y)
        return rect


#################################################

class Menu( StarObject ) :

    icons = None
    menus = {}

    def __init__( self, game, menu_items ) :
        "menu_items: list of MenuItem"
        StarObject.__init__( self, game, Stationary( None ), 0, 0 )
        self.menu_items = menu_items
        self.focused = None
        self.visible = False
        self.size = 200
        self.age = 0

    def repaint(self, win ):
        if not self.visible : 
            return
        self.current_zoom = Game.approach_value( self.current_zoom, 1, 4 )
        self.current_angle = Game.approach_value( self.current_angle, 45, 6 )
        self.repaint_engine(win, self.current_zoom, self.current_angle )

    def repaint_engine(self, win, zoom=1.0, angle_increment=30):
        num_items = len(self.menu_items)
        radius = 40 * zoom  # Adjust the radius based on the zoom factor

        # Convert spread from degrees to radians and divide by the number of items
        angle_increment = math.radians(angle_increment)

        (xx,yy) = self.game.get_display_xy( self.x, self.y, 0 )

        for i, item in enumerate(self.menu_items):
            # Calculate the angle in radians, starting at 10 o'clock direction (-2/3 pi)
            angle = -2/3 * math.pi + i * angle_increment

            # Calculate the position of the menu item
            item_x = xx + radius * math.cos(angle)
            item_y = yy + radius * math.sin(angle)

            item.set_pos(item_x, item_y)

            # Draw the menu item's icon at the calculated position
            icon = item.get_frame( item == self.focused )

            icon = pygame.transform.scale(icon, (int(icon.get_width() * zoom), int(icon.get_height() * zoom))) # Scale the icon based on the zoom factor
            icon_rect = icon.get_rect(center=(item_x, item_y))
            win.blit(icon, icon_rect.topleft)

            # pygame.draw.rect(win, (255,0,0), item.get_collision_rect())


    def ticktack(self) :
        self.age += 1
        if self.age > 5000 :
            self.hide()
        super().ticktack()

    def show_at(self, x, y) :
        self.set_pos(x, y)
        self.visible = True
        self.current_zoom = 0
        self.current_angle = 0
        self.age = 0
        self.game.set_mouse_tracking(self, True)

    def hide(self) :
        if not self.visible : return
        self.visible = False
        self.game.set_mouse_tracking(self, False)
        self.game.remove_object(self)

    def mouse_track(self, game_coords, screen_coords) :
        for item in self.menu_items:
            rect = item.get_collision_rect()
            # print(f'    check rect {rect}')
            if item.get_collision_rect().collidepoint(*screen_coords) :
                self.focused = item
                return
        self.focused = None


    @staticmethod
    def selected( menu_item ) :
        print(f'selected menu_item: {menu_item}')

    @staticmethod
    def target_menu(game, x, y) :
        if Menu.icons == None :
            Menu.icons = AnimatedSprite( "iconsheet-menu.png", 11, 2, MenuItem.ICON_SIZE, True )
        menu = Menu.menus.get('target')
        if menu == None :
            menu = Menu(game, 
                [ 
                    MenuItem( Menu.icons, 5, 16, "move", Menu.selected ),
                    MenuItem( Menu.icons, 1, 12, "attack", Menu.selected ),
                    MenuItem( Menu.icons, 4, 15, "flee", Menu.selected ),
                ]
            )
            Menu.menus['target'] = menu
        menu.show_at(x, y)
        return menu

