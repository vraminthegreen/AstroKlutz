
import pygame

from StarObject import StarObject
from ShipClass import ObjectClass
from Menu import Menu, MenuItem
from Targets import TargetGroupMove, TargetGroupAttackMove, TargetGroupPatrolMove, TargetGroupEnemyEscape


class Group( StarObject ) :

    groups = [ None, None, None, None, None, None, None, None, None ]

    def __init__(self, game, team, number = None) :
        super().__init__(game, ObjectClass(), 0, 0)
        self.visible = False
        self.focus_visible = True
        self.ships = []
        self.bounding_rect = pygame.Rect(0,0,0,0)
        if number == None :
            self.number = Group.groups.index(None) + 1
        else :
            self.number = number
        Group.groups[self.number-1] = self
        self.background_color = [0, 128, 128, 64]
        self.background_color2 = [0, 128, 128, 120]
        self.minimized_size = 32
        self.game.register_key_handler( str(self.number), self )
        self.select_animation = None
        self.team = team
        self.name = "Team-" + self.team.get_new_name()

    def add_ship(self,ship) :
        if ship in self.ships :
            return
        self.ships.append(ship)
        if len(self.ships) == 1 :
            self.visible = True
            self.game.add_object(self)
        ship.add_on_dead_listener( self )
        for order in self.orders :
            order.add_ship(ship)
        if len(self.ships) == 1 :
            self.bounding_rect = ship.get_rect()
        else :
            self.bounding_rect.union_ip(ship.get_rect())
        self.visible = True
        (self.x,self.y) = self.bounding_rect.center
        self.size = max(self.bounding_rect.width, self.bounding_rect.height)

    def remove_ship(self,ship) :
        ship.remove_on_read_listener( self )
        self.ships.remove(ship)
        for order in self.orders :
            order.remove_ship(ship)
        if len(self.ships) == 0 :
            self.visible = False
            self.game.remove_object( self )
            return
        self.update_bounding_rect()

    def remove_all(self) :
        for ship in self.ships :
            ship.remove_on_read_listener(self)
        self.orders = []
        self.ships = []
        self.visible = False
        self.game.remove_object(self)

    def is_empty(self) :
        return len(self.ships) == 0

    def on_dead(self, ship) :
        self.remove_ship(ship)

    def update_bounding_rect(self) :
        self.bounding_rect = self.ships[0].get_rect()
        for aship in self.ships[1:] :
            self.bounding_rect.union_ip(aship.get_rect())
        (self.x,self.y) = self.bounding_rect.center
        self.size = max(self.bounding_rect.width, self.bounding_rect.height)

    def get_rect(self) :
        return self.bounding_rect

    def ticktack(self) :
        if self.select_animation != None :
            self.select_animation -= 1
            if self.select_animation < 0 :
                self.select_animation = None
        if self.game.get_focused() == self :
            refresh = 1
        else :
            refresh = 50
        if self.game.get_time() % refresh == 0 :
            self.update_bounding_rect()
        super().ticktack()

    def repaint(self, win):
        # Calculate group's position and size based on its number
        group_height = self.minimized_size + 10  # 10 for padding
        group_y = 10 + (self.number) * group_height  # 10 for top margin
        group_width = len(self.ships) * self.minimized_size + 30  # 30 for padding and number

        bg = self.background_color
        if self.select_animation != None and ( ( self.select_animation // 3 ) % 2 == 0 ) :
            bg = self.background_color2

        # Draw semi-transparent background
        background_rect = pygame.Surface((group_width, group_height), pygame.SRCALPHA)
        background_rect.fill(bg)
        win.blit(background_rect, (10, group_y))  # 10 for left margin

        # Draw group number
        if self.number > 0 :
            font = pygame.font.Font(None, self.minimized_size)  # Use default font
            number_surface = font.render(str(self.number), True, (50, 255, 200))
            win.blit(number_surface, (15, group_y + 10))  # 15 for left margin, 5 for top padding

        # Draw ship miniatures
        icon_x = 35
        for i, ship in enumerate(self.ships):
            if ship.icon == None : continue # for example exploding ship
            icon = pygame.transform.scale(ship.icon, (ship.minimized_size, ship.minimized_size))
            rotated_icon = pygame.transform.rotate(icon, 90)  # Rotate icon by -90 degrees
            win.blit(rotated_icon, (icon_x, group_y + 5 + (self.minimized_size - ship.minimized_size)/2))  # 5 for top padding
            icon_x += ship.minimized_size + 5  # 30 for left margin and number

    def draw_select( self, win, color ) :
        for ship in self.ships :
            ship.draw_select( win, color )

    def on_key_pressed( self, key ) :
        if key != str(self.number) :
            return
        self.game.set_focused( self )
        self.select_animation = 20

    def is_hostile(self, other) :
        return self.team != other.team

    def click( self, x, y ) :
        self.current_menu_pos = (x,y)
        objs = self.game.get_objects_in_range(x, y, 20)
        print(f'click selected {len(objs)} elements: {objs}')
        for obj in objs :
            if obj.is_hostile(self) :
                menu = Menu.enemy_menu(self.game, x, y, self, obj)
            else :
                menu = Menu.group_friend_menu(self.game, x, y, self, obj)
            self.game.push_focused( menu )
            return True

        menu = Menu.target_menu(self.game, x, y, self)
        self.game.push_focused( menu )
        return True

    def order_guard(self, x, y, menu_item = None) :
        order = TargetGroupAttackMove( self.game, self, x, y, menu_item, 1000 )
        self.append_order( order )

    def on_menu(self, menu_item, target) :
        order = None
        if menu_item.command == MenuItem.FRIEND_GROUP :
            if target in self.ships :
                self.remove_ship( target )
                if len(self.ships) == 0 :
                    self.game.remove(self)
            else :
                self.add_ship( target )
        elif menu_item.command == MenuItem.MOVE :
            order = TargetGroupMove( self.game, self, *self.current_menu_pos, menu_item )
        elif menu_item.command == MenuItem.ATTACK :
            order = TargetGroupAttackMove( self.game, self, *self.current_menu_pos, menu_item )
        elif menu_item.command == MenuItem.PATROL :
            order = TargetGroupPatrolMove( self.game, self, *self.current_menu_pos, menu_item )
        elif menu_item.command == MenuItem.GUARD :
            self.order_guard( *self.current_menu_pos )

        # elif menu_item.command == MenuItem.FLEE :
        #     order = TargetEscape(self.game, self, Stationary('escape', 32), *self.current_menu_pos, menu_item )
        # elif menu_item.command == MenuItem.FRIEND_FOLLOW :
        #     order = TargetFollow(self.game, self, Stationary('move', 32), menu_item, target, False)
        # elif menu_item.command == MenuItem.FRIEND_GUARD :
        #     order = TargetFollow(self.game, self, Stationary('protect', 24), menu_item, target, True)
        # elif menu_item.command == MenuItem.ENEMY_ATTACK :
        #     order = TargetAttack(self.game, self, Stationary('target', 32), menu_item, target )
        elif menu_item.command == MenuItem.ENEMY_FLEE :
            order = TargetGroupEnemyEscape(self.game, self, menu_item, target)
        # elif menu_item.command == MenuItem.FRIEND_GROUP :
        #     Group.new(self.game, self)
        else :
            print(f'menu clicked: {menu_item.label}, NOT HANDLED')
            return False
        if order != None :
            self.append_order( order )


    @staticmethod
    def new(game, ship) :
        group = Group(game, ship.team)
        game.add_object(group)
        group.add_ship(ship)
        game.set_focused(group)
        return group



