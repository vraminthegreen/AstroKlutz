

class Pilot :

    def __init__(self, game) :
        self.enemy = None
        self.game = game

    def set_enemy(self, enemy) :
        self.enemy = enemy

    def set_starship(self, starship) :
        self.starship = starship

    def ticktack(self) :
        pass

#################################################

class FighterPilot ( Pilot ) :

    def __init__(self, game) :
        Pilot.__init__(self, game)
        self.enemy_chase_mode = 1
        self.chase_pos = None

    def set_enemy(self, enemy) :
        self.enemy = enemy
        self.chase_pos = None

    def ticktack(self) :
        if self.enemy == None :
            return
        if self.game.get_time() % 50 == 0 or self.chase_pos == None :
            if self.enemy_chase_mode == 1 :
                self.chase_pos = self.enemy.get_pos_in_front(-300)
            else :
                self.chase_pos = self.enemy.get_pos()
            if self.enemy.is_in_field(self.starship.x, self.starship.y, self.starship.dir - (180+45), self.starship.dir - (180-45), 0, 500) :
                self.enemy_chase_mode = 2
            elif not self.enemy.is_in_field(self.starship.x, self.starship.y, self.starship.dir - (180+60), self.starship.dir - (180-60), 0, 500) :
                self.enemy_chase_mode = 1
        self.starship.chase( *self.chase_pos )
        if self.game.get_time() % 10 == 0 and self.starship.is_in_field( self.enemy.x, self.enemy.y, self.starship.dir - 30, self.starship.dir + 30, 0, 250) :
            self.starship.fire()

#################################################

class RocketFrigatePilot ( Pilot ) :

    def __init__(self, game) :
        Pilot.__init__(self, game)

    def ticktack(self) :
        if self.enemy == None :
            return
        (pos1x, pos1y) = self.enemy.get_displaced_pos(self.enemy.dir+90,200)
        (pos2x, pos2y) = self.enemy.get_displaced_pos(self.enemy.dir-90,200)
        if self.starship.distance_to_xy(pos1x,pos1y) < self.starship.distance_to_xy(pos2x,pos2y) :
            self.starship.chase( pos1x, pos1y )
        else :
            self.starship.chase( pos2x, pos2y )
        if self.game.get_time() % 200 <= 1 and self.starship.distance_to( self.enemy ) < 500:
            self.starship.fire_missile()


#################################################

class MissilePilot ( Pilot ) :

    def __init__(self, game) :
        Pilot.__init__(self, game)
        self.enemy_chase_mode = 1        

    def ticktack(self) :
        if self.starship.fuel > 0 :
            self.starship.fuel -= 1
            if self.starship.enemy == None :
                self.starship.explode()
                return
            order_hit = self.starship.distance_to(self.starship.enemy) < self.starship.get_size()
            if self.starship.fuel == 0 or order_hit :
                self.starship.fuel = 0
                if order_hit :
                    self.starship.enemy.hit( self.starship )
                self.starship.explode()
            else :
                (self.starship.maxV, self.starship.rotation_speed, self.starship.maxAcc) = self.starship.object_class.select_phase(self.starship.fuel)
                self.starship.chase(self.starship.enemy.x, self.starship.enemy.y)                


