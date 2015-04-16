from pokemon import Pokemon

class PokeList:
	def __init__(self):
		self.pokemon = []
		self.unknown_init()
		
	def unknown_init(self):
		self.unknown = Pokemon()
		self.unknown.set_name('???')
		self.unknown.set_type('???')
		self.unknown.set_stats(['???','???','???','???','???','???','???'])
		self.unknown.set_weaknesses([['???'],['???'],['???'],['???'],['???'],['???']])
		self.unknown.set_image()
	
	def get_unknown(self):
		return self.unknown
	
	def get_all(self):
		if len(self.pokemon):
			return self.pokemon
		else:
			return [self.unknown]
	
	def add(self,pokemon):
		for stored_pokemon in self.pokemon:
			if stored_pokemon.get_name().lower() == pokemon.get_name().lower():
				return
		self.pokemon.append(pokemon)
	
	def add_one(self,item):
		pokemon = Pokemon()
		pokemon.set_name(item[0])
		pokemon.set_type(item[1])
		pokemon.set_stats(item[2])
		if len(item) == 3:
			pokemon.set_weaknesses(self.unknown.get_weaknesses())
		else:
			pokemon.set_weaknesses(item[3])
		pokemon.set_image()
		self.pokemon.append(pokemon)
		
	def add_all(self,items):
		for index,item in enumerate(items):
			pokemon = Pokemon()
			pokemon.set_name(item[0])
			pokemon.set_type(item[1])
			pokemon.set_stats(item[2])
			if len(item) == 3:
				pokemon.set_weaknesses(self.unknown.get_weaknesses())
			else:
				pokemon.set_weaknesses(item[3])
			pokemon.set_image()
			pokemon.set_index(index)
			self.pokemon.append(pokemon)
		
	def name_filter(self,string):
		subset = []
		for pokemon in self.pokemon:
			if string in pokemon.get_name().lower():
				subset.append(pokemon)
		if len(subset) == 0:
			subset.append(self.unknown)
		return subset
	
	def type_filter(self,string):
		strings = string.split(' ')
		subset = []
		for pokemon in self.pokemon:
			is_in = 0
			for substring in strings:
				if substring in pokemon.get_type().lower():
					is_in += 1
			if len(strings) == is_in:
				subset.append(pokemon)
		if len(subset) == 0:
			subset.append(self.unknown)
		return subset
	
	def remove(self,name):
		for index,pokemon in enumerate(self.pokemon):
			if pokemon.get_name().lower() == name.lower():
				del self.pokemon[index]
				break
	
	def get(self,name):
		for pokemon in self.pokemon:
			if pokemon.get_name().lower() == name.lower():
				return pokemon
		return self.unknown