

class Team :

	def __init__(self, name, color, number) :
		self.name = name
		self.color = color
		self.number = number

	def get_filename_sufix(self) :
		return '_' + str(self.number)
		