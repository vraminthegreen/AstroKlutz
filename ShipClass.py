
class ShipClass :

    pass

#################################################
        
class FighterClass :

    def __init__(self) :
        self.icon_name = "fighter"
        self.size = 48
        self.max_bullets = 5
        self.front_shield = 90
        self.rear_shield = 50
        self.maxV = 3  # Maximum speed
        self.rotation_speed = 1.5
        self.maxAcc = 0.03
        self.resistance = 0.99 # thrusters power
        self.can_be_hit = True


class MissileClass :

    def __init__(self) :
        self.icon_name = "missile"
        self.size = 48
        self.maxV = 1  # Maximum speed
        self.rotation_speed = 0.5
        self.maxAcc = 0.03 # thrusters power
        self.resistance = 0.99 # thrusters power
        self.chaseDecelerate = True
        self.fuel = 700
        self.can_be_hit = True


class BulletClass :

    def __init__(self) :
        self.icon_name = None
        self.size = 2
        self.fuel = 100
        self.resistance = 1
        self.can_be_hit = False


class Stationary :

    def __init__(self, icon_name) :
        self.icon_name = icon_name
        self.size = 48
        self.resistance = 1
        self.can_be_hit = False

        # self.maxV = 1  # Maximum speed
        # self.rotation_speed = 0.5
        # self.maxAcc = 0.03 # thrusters power
        # self.chaseDecelerate = True
