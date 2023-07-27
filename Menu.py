
import pygame
import math

from Game import Game
from StarObject import StarObject
from ShipClass import Stationary
from AnimatedSprite import AnimatedSprite

#################################################

class MenuItem :

    ICON_SIZE = 32

    MOVE = 1
    ATTACK = 2
    FLEE = 3
    ENEMY_ATTACK = 4
    ENEMY_FLEE = 5
    FRIEND_FOLLOW = 6
    FRIEND_GUARD = 7
    PATROL = 8
    FRIEND_GROUP = 9
    GUARD = 10

    def __init__( self, icon, not_selected, selected, label, command ) :
        """
        icon: AnimatedSprite
        not_selected: number of frame for not selected
        selected: number of frame for selected
        """
        self.command = command
        self.icon = icon
        self.label = label
        self.selected = selected
        self.not_selected = not_selected
        self.x = 0
        self.y = 0

    def get_frame( self, focused ) :
        frameno = self.selected if focused else self.not_selected
        return self.icon.get_frame( frameno )

    def set_pos(self, x, y) :
        self.x = x
        self.y = y

    def get_collision_rect(self, range = 0.7) :
        rect = pygame.Rect(0, 0, MenuItem.ICON_SIZE*range, MenuItem.ICON_SIZE*range)
        rect.center = (self.x, self.y)
        return rect


#################################################

class Menu( StarObject ) :

    DEFAULT_RADIUS = 40
    icons = None
    menus = {}
    active_menu = None

    def __init__( self, game, menu_items ) :
        "menu_items: list of MenuItem"
        StarObject.__init__( self, game, Stationary( None ), 0, 0 )
        self.menu_items = menu_items
        self.reset()

    def reset(self) :
        self.current_zoom = 0
        self.current_angle = 0
        self.age = 0
        self.focused = None
        self.clicked = None
        self.size = 200
        self.not_clicked_radius = Menu.DEFAULT_RADIUS
        self.not_clicked_zoom = 1
        self.select_age = None
        self.visible = False
        self.hiding = False
        self.owner = None
        self.target = None

    def repaint(self, win ):
        if not self.visible : 
            return
        if self.hiding :
            self.current_zoom = Game.approach_value( self.current_zoom, 0, 5 )                
            self.not_clicked_radius = Game.approach_value( self.not_clicked_radius, 0, 5 )
        elif self.clicked != None :
            self.not_clicked_radius = Game.approach_value( self.not_clicked_radius, Menu.DEFAULT_RADIUS * 0.5, 6 )
            self.not_clicked_zoom = Game.approach_value( self.not_clicked_zoom, 0.7, 6 )
            if self.age - self.select_age > 20 :
                self.current_zoom = Game.approach_value( self.current_zoom, 0, 4 )                
        else :
            self.current_zoom = Game.approach_value( self.current_zoom, 1, 4 )
            self.current_angle = Game.approach_value( self.current_angle, 45, 6 )
        self.repaint_engine(win, self.current_zoom, self.current_angle )

    def repaint_engine(self, win, zoom=1.0, angle_increment=30):
        # print(f'repaint_engine, time: {self.game.get_time()}')
        num_items = len(self.menu_items)
        radius = Menu.DEFAULT_RADIUS * zoom  # Adjust the radius based on the zoom factor

        # Convert spread from degrees to radians and divide by the number of items
        angle_increment = math.radians(angle_increment)

        (xx,yy) = self.game.get_display_xy(self.x, self.y, 0)

        for i, item in enumerate(self.menu_items):
            # Calculate the angle in radians, starting at 10 o'clock direction (-2/3 pi)
            angle = -2/3 * math.pi + i * angle_increment

            # Calculate the position of the menu item
            if not self.hiding and ( self.clicked == None or self.clicked == item ) :
                theradius = radius
                thezoom = zoom
            else :
                theradius = self.not_clicked_radius
                thezoom = self.not_clicked_zoom * zoom
            item_x = xx + theradius * math.cos(angle)
            item_y = yy + theradius * math.sin(angle)

            item.set_pos(item_x, item_y)

            # Draw the menu item's icon at the calculated position
            icon = item.get_frame( 
                item == self.focused 
                or item == self.clicked and (self.age // 3) % 2 == 0 )

            icon = pygame.transform.scale(icon, (int(icon.get_width() * thezoom), int(icon.get_height() * thezoom))) # Scale the icon based on the zoom factor
            icon_rect = icon.get_rect(center=(item_x, item_y))
            win.blit(icon, icon_rect.topleft)
            # pygame.draw.rect(win, (255,0,0), item.get_collision_rect())

    def select(self, clicked_item) :
        if clicked_item == None : 
            self.on_focus_lost()
            return
        self.clicked = clicked_item
        print(f'select, owner = {self.owner}')
        if self.owner != None :
            print(f'calling on_menu')
            self.owner.on_menu( self.clicked, self.target )
        self.focused = None
        self.select_age = self.age

    def ticktack(self) :
        self.age += 1
        if ( self.clicked != None or self.hiding ) and self.current_zoom == 0 :
            print("KONIEC MENU")
            self.hide()
        super().ticktack()

    def show_at(self, x, y) :
        self.set_pos(x, y)
        self.visible = True
        self.game.add_object(self)
        self.game.set_mouse_tracking(self, True)

    def hide(self) :
        if not self.visible : return
        self.visible = False
        self.game.set_mouse_tracking(self, False)
        self.game.remove_object(self)

    def get_item_at(self, scr_x, scr_y) :
        for item in self.menu_items:
            rect = item.get_collision_rect()
            # print(f'    check rect {rect}')
            if item.get_collision_rect().collidepoint(scr_x, scr_y) :
                return item
        return None

    def mouse_track(self, game_coords, screen_coords) :
        if self.clicked or self.hiding : 
            return
        self.focused = self.get_item_at(*screen_coords)

    def click( self, game_x, game_y ) :
        if self.clicked or self.hiding :
            print(f'Menu.click: ignored')
            return True
        print(f'Menu.click: accepted')
        scr_pos = self.game.get_display_xy( game_x, game_y )
        self.select( self.get_item_at( *scr_pos ) )
        return True

    def on_focus_lost( self ) :
        if self.clicked or self.hiding :
            return
        self.hiding = True

    def set_owner( self, owner ) :
        self.owner = owner

    def set_target( self, target ) :
        self.target = target

    def activate( self, x, y, owner, target ) :
        self.reset()
        self.show_at(x, y)
        self.set_owner( owner )
        self.set_target( target )
        Menu.active_menu = self
        return self

    @staticmethod
    def selected( menu_item ) :
        print(f'selected menu_item: {menu_item}')

    @staticmethod
    def reset_menu() :
        if Menu.active_menu != None :
            Menu.active_menu.hide()
        if Menu.icons == None :
            Menu.icons = AnimatedSprite( "iconsheet-menu.png", 11, 2, MenuItem.ICON_SIZE, True )

    @staticmethod
    def target_menu(game, x, y, owner) :
        Menu.reset_menu()
        menu = Menu.menus.get('target')
        if menu == None :
            menu = Menu(game, 
                [ 
                    MenuItem( Menu.icons, 5, 16, "move",   MenuItem.MOVE ),
                    MenuItem( Menu.icons, 1, 12, "attack", MenuItem.ATTACK ),
                    MenuItem( Menu.icons, 7, 18, "patrol", MenuItem.PATROL ),
                    MenuItem( Menu.icons, 2, 13, "guard", MenuItem.GUARD ),
                    MenuItem( Menu.icons, 4, 15, "flee",   MenuItem.FLEE ),
                ]
            )
            Menu.menus['target'] = menu
        return menu.activate(x, y, owner, None)


    @staticmethod
    def enemy_menu(game, x, y, owner, target) :
        Menu.reset_menu()
        menu = Menu.menus.get('enemy')
        if menu == None :
            menu = Menu(game, 
                [ 
                    MenuItem( Menu.icons, 1, 12, "attack", MenuItem.ENEMY_ATTACK ),
                    MenuItem( Menu.icons, 4, 15, "flee",   MenuItem.ENEMY_FLEE ),
                ]
            )
            Menu.menus['enemy'] = menu
        return menu.activate(x, y, owner, target)

    @staticmethod
    def friend_menu(game, x, y, owner, target) :
        Menu.reset_menu()
        menu = Menu.menus.get('friend')
        if menu == None :
            menu = Menu(game, 
                [ 
                    MenuItem( Menu.icons, 5, 16, "follow", MenuItem.FRIEND_FOLLOW ),
                    MenuItem( Menu.icons, 2, 13, "guard",   MenuItem.FRIEND_GUARD ),
                ]
            )
            Menu.menus['friend'] = menu
        return menu.activate(x, y, owner, target)

    @staticmethod
    def group_friend_menu(game, x, y, owner, target) :
        Menu.reset_menu()
        menu = Menu.menus.get('group_friend')
        if menu == None :
            menu = Menu(game, 
                [ 
                    MenuItem( Menu.icons, 5, 16, "follow", MenuItem.FRIEND_FOLLOW ),
                    MenuItem( Menu.icons, 2, 13, "guard", MenuItem.FRIEND_GUARD ),
                    MenuItem( Menu.icons, 9, 20, "group", MenuItem.FRIEND_GROUP ),                   
                ]
            )
            Menu.menus['group_friend'] = menu
        return menu.activate(x, y, owner, target)

    @staticmethod
    def self_menu(game, x, y, owner ) :
        Menu.reset_menu()
        menu = Menu.menus.get('self')
        if menu == None :
            menu = Menu(game, 
                [ 
                    MenuItem( Menu.icons, 9, 20, "group", MenuItem.FRIEND_GROUP ),
                ]
            )
            Menu.menus['self'] = menu
        return menu.activate(x, y, owner, owner)
