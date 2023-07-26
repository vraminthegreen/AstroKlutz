

class Team :

    CODES = [
    "Alfa",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliett",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whiskey",
    "X-ray",
    "Yankee",
    "Zulu"
    ]

    def __init__(self, name, color, number) :
        self.name = name
        self.color = color
        self.number = number
        self.names = [ "Alfa", "Bravo", "Delta"]
        self.counter = 0

    def get_filename_sufix(self) :
        return '_' + str(self.number)
        
    def get_new_name(self) :
        if self.counter < len(Team.CODES) :
            res = Team.CODES[self.counter] + "-" + self.name
        else :
            res = str(self.counter) + "-" + self.name
        self.counter += 1
        return res
