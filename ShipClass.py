
class ObjectClass :

    def __init__(self) :
        self.layer = 0
        self.detectors_range = 0
        self.layer = 0
        self.size = 0
        self.minimized_size = 0
        self.can_be_hit = False
        self.resistance = 1
        self.maxAcc = 1
        self.maxV = 1
        self.rotation_speed = 1
        self.chaseDecelerate = False
        self.icon_name = None
        self.is_important = False


#################################################
        
class FighterClass ( ObjectClass ) :

    def __init__(self) :
        ObjectClass.__init__(self)
        self.icon_name = "fighter"
        self.size = 48
        self.minimized_size = 24
        self.max_bullets = 5
        self.max_missiles = 0
        self.front_shield = 90
        self.rear_shield = 50
        self.maxV = 3  # Maximum speed
        self.rotation_speed = 1.75
        self.maxAcc = 0.03
        self.resistance = 0.99 # thrusters power
        self.can_be_hit = True
        self.chaseDecelerate = True
        self.detectors_range = 250
        self.is_important = True

#################################################

class RocketFrigateClass ( ObjectClass ) :

    def __init__(self) :
        ObjectClass.__init__(self)
        self.icon_name = "rocket"
        self.size = 64
        self.minimized_size = 32
        self.max_bullets = 0
        self.max_missiles = 2
        self.front_shield = 80
        self.rear_shield = 30
        self.maxV = 1.5  # Maximum speed
        self.rotation_speed = 0.75
        self.maxAcc = 0.02
        self.resistance = 0.99 # thrusters power
        self.can_be_hit = True
        self.chaseDecelerate = True
        self.detectors_range = 700
        self.is_important = True

#################################################

class MissileClass ( ObjectClass ) :

    def __init__(self) :
        ObjectClass.__init__(self)
        self.icon_name = "missile"
        self.size = 32
        self.maxV = 5  # Maximum speed
        self.rotation_speed = 0.1
        self.maxAcc = 0.2 # thrusters power

        self.phase = {
            0: (2, 1, 0.03),
            1: (self.maxV,self.rotation_speed,self.maxAcc)
        }
        self.resistance = 1
        self.chaseDecelerate = False
        self.fuel = 300
        self.can_be_hit = True

    def select_phase(self, current_fuel) :
        if current_fuel > self.fuel - 150 : 
            return self.phase[0]
        else : 
            return self.phase[1]

    def get_max_v(self, current_fuel) :
        self.select_phase(current_fuel)[0]

    def get_rotation_speed(self, current_fuel) :
        self.select_phase(current_fuel)[1]

    def get_max_acc(self, current_fuel) :
        self.select_phase(current_fuel)[2]

#################################################

class BulletClass ( ObjectClass ) :

    def __init__(self) :
        ObjectClass.__init__(self)
        self.icon_name = None
        self.size = 3
        self.fuel = 100
        self.resistance = 1
        self.can_be_hit = False
        self.maxV = 5  # Maximum speed
        self.rotation_speed = 0
        self.maxAcc = 0 # thrusters power
        self.chaseDecelerate = False

#################################################

class DustClass( ObjectClass ) :

    def __init__(self) :
        ObjectClass.__init__(self)
        self.icon_name = None
        self.size = 1
        self.resistance = 1
        self.can_be_hit = False
        self.maxV = 0  # Maximum speed
        self.rotation_speed = 0
        self.maxAcc = 0 # thrusters power
        self.chaseDecelerate = False

#################################################

class Stationary ( ObjectClass ) :

    def __init__(self, icon_name, size = None) :
        ObjectClass.__init__(self)
        self.icon_name = icon_name
        self.size = size
        self.resistance = 1
        self.can_be_hit = False
        self.chaseDecelerate = False
        self.maxV = 0  # Maximum speed
        self.rotation_speed = 0
        self.maxAcc = 0

#################################################

class Background ( Stationary ) :

    def __init__(self) :
        Stationary.__init__(self, None, None)
        self.layer = 5

