

class Pilot :

    def __init__(self, game) :
        self.enemy = None
        self.game = game

    def get_icon_name(self) :
        return "fighter"
        
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

    def get_icon_name(self) :
        return "fighter"

    def ticktack(self) :
        if self.enemy != None :
            if self.enemy_chase_mode == 1 :
                self.starship.chase( * self.enemy.get_pos_in_front(-200) )
            else :
                self.starship.chase( * self.enemy.get_pos() )
            if self.enemy.is_in_field(self.starship.x, self.starship.y, self.starship.dir - (180+25), self.starship.dir - (180-25), 0, 300) :
                self.enemy_chase_mode = 2
            elif not self.enemy.is_in_field(self.starship.x, self.starship.y, self.starship.dir - (180+45), self.starship.dir - (180-45), 0, 300) :
                self.enemy_chase_mode = 1
            if self.game.get_time() % 10 == 0 and self.starship.is_in_field( self.enemy.x, self.enemy.y, self.starship.dir - 30, self.starship.dir + 30, 0, 250) :
                self.starship.fire()


