import pygame
import os
import math
import random

from StarObject import StarObject
from Bullet import Bullet
from Missile import Missile
from ShipClass import MissileClass, Stationary
from Pilot import MissilePilot
from Game import Game
from IconRepository import IconRepository
from Menu import Menu, MenuItem
from Targets import TargetMove, TargetAttack



class Starship ( StarObject ) :

    def __init__(self, game, team, object_class, pilot, x, y ):
        StarObject.__init__( self, game, object_class, x, y )
        self.team = team
        self.pilot = pilot
        self.pilot.set_starship( self )
        self.icon = IconRepository.get_icon( self.object_class.icon_name, self.get_size(), self.team )
        self.dir = -150
        self.bullets = []
        self.missiles = []
        self.enemy = None
        self.dead = False
        self.shield_active = False
        self.is_important = True
        self.is_selectable = True
        self.focus_visible = True
        self.ping_animation = None

    def is_hostile(self, other) :
        return self.team != other.team

    def command( self, cmd ) :
        if cmd == 'a' :
            if self.auto != None and self.order != None:
                self.game.remove_object(self.order)
                self.order = None
            self.auto = not self.auto
            return True
        elif cmd == 't' :
            print("PING")
            self.ping_animation = 100
            return True
        elif cmd == ' ' :
            self.fire()
            return True
        return False

    def fire( self ) :
        if len(self.bullets) < self.object_class.max_bullets :
            bullet = Bullet( self.game, self, self.x, self.y, self.dir, self.v )
            self.bullets.append( bullet )
            self.game.add_object( bullet )

    def fire_missile( self ) :
        missiles_cnt = len(self.missiles)
        if missiles_cnt < self.object_class.max_missiles :
            missile_dir = ( self.dir + 150 + 60 * ( missiles_cnt % 2 ) ) % 360
            (mx, my) = self.get_displaced_pos(missile_dir,self.size)
            missile = Missile(self.game, MissileClass(), MissilePilot(self.game), mx, my )
            missile.set_order(self.enemy)
            missile.set_owner(self)
            missile.dir = missile_dir
            self.missiles.append( missile )
            self.game.add_object(missile)

    def on_missile_exploded( self, missile ) :
        self.missiles.remove( missile )

    def remove_object( self, obj ) :
        self.bullets.remove( obj )
        self.game.remove_object( obj )

    def set_enemy( self, enemy ) :
        self.enemy = enemy
        self.pilot.set_enemy( enemy )

    def ping_logic(self) :
        if self.ping_animation == None :
            return
        if self.enemy != None :
            self.ping_animation = None
            return
        self.ping_animation -= 2
        if self.ping_animation < 0 : 
            self.ping_animation = None
            objs = self.game.get_objects_in_range(self.x, self.y, self.detectors_range)
            for obj in objs :
                if self.is_hostile(obj) :
                    print("FOUND ENEMY")
                    self.set_enemy(obj)

    def order_logic(self) :
        if len(self.orders) == 0 :
            return
        self.orders[0].logic(self)

    def ticktack(self):
        self.ping_logic()
        self.order_logic()
        self.pilot.ticktack()
        super().ticktack()

    def hit(self, hitter):
        if self.dead or self.shield_active : return
        ddiff = ( hitter.dir - self.dir - 180 ) % 360
        if ddiff < 0 : ddiff = -ddiff
        aa = Game.is_acute_angle( hitter.dir, self.dir )
        if aa :
            print("belly hit")
        else :
            print("shield hit")
        if ( aa and random.randint(0, 99) < (100-self.object_class.rear_shield) ) or ( random.randint(0,99) < (100-self.object_class.front_shield) ) :
            self.icon = None
            self.dead = True
            self.animate( self.game.get_animation('explosion'), Starship.onExploded )
        else :
            self.shield_active = True
            self.animate( self.game.get_animation('shield'), Starship.onShieldEnded )

    def onExploded( self ) :
        self.game.remove_object( self )

    def onShieldEnded( self ) :
        self.shield_active = False

    def click( self, x, y ) :
        print(f'create menu at ({x},{y})')
        self.current_menu_pos = (x,y)
        menu = Menu.target_menu(self.game, x, y, self)
        self.game.push_focused( menu )

    def on_menu(self, menu_item) :
        if menu_item.command == MenuItem.MOVE :
            order = TargetMove(self.game, Stationary('move',32), *self.current_menu_pos, menu_item )
            self.append_order( order )
        elif menu_item.command == MenuItem.ATTACK :
            order = TargetAttack(self.game, Stationary('target', 40), *self.current_menu_pos, menu_item )
            self.append_order( order )
        else :
            print(f'menu clicked: {menu_item.label}, NOT HANDLED')
            return False

    def repaint_ping(self, win) :
        if self.ping_animation == None :
            return
        temp_surface = pygame.Surface((200,200), pygame.SRCALPHA)
        # Compute the transparency
        transparency = int((0.5*self.ping_animation+50)*2.55)  # Scale from 0-100 to 0-255
        # Draw the circle on the temporary surface
        pygame.draw.circle(temp_surface, (0,200,255,transparency), (100,100), 100-self.ping_animation, 1)
        # Blit the temporary surface onto the main surface
        gpos = self.game.get_display_xy(self.x, self.y)
        win.blit(temp_surface, (gpos[0]-100, gpos[1]-100))  # Adjust the position as needed


    def repaint(self, win) :
        self.repaint_ping(win)
        super().repaint(win)

    # # Update the display
    # pygame.display.flip()



    # def repaint(self, win):
    #     if self.enemy != None :
    #         (xx,yy) = self.enemy.get_pos_in_front(-100)
    #         pygame.draw.rect(win, (255, 255, 255), pygame.Rect(xx, yy, 5, 5))
    #     super().repaint(win)


