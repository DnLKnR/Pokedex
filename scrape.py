import urllib


class Scrape:
	def __init__(self):
		self.all_data = []
	def scrape(self):
		url1 = 'http://pokemondb.net/pokedex/all'
		url2 = 'http://www.pokeffectiveness.com/'
		self.html1 = urllib.urlopen(url1).read()
		self.html2 = urllib.urlopen(url2).read()
		file = open('pokedata.cfg','w')
		self.getStats()
		self.getWeaknesses()
		for idx,val in enumerate(self.all_data):
			if len(val) == 3:
				self.FixWeakness(idx)
		all_data_str = str(self.all_data).replace(', \'',',\'')
		file.write(all_data_str)
		file.close()
		self.reset(self.all_data)
		
	def getStats(self):
		self.all_data = []
		temp = str(self.html1)
		tempData = temp.split("<td class=\"num cell-icon-string\" ")[1:]
		idx = 0
		for v in tempData:
			poke = v.split('/pokedex/')
			pokenames = poke[1].split('"')
			poke_name = pokenames[0].strip().title()
			if '"aside">' in v:
				special_name_list = v.split('"aside">')
				special_name_list = special_name_list[1].split('<')
				special_name = special_name_list[0]
				if poke_name in special_name.title():
					poke_name = special_name.strip().title()
				else:
					poke_name += ' (' + special_name.strip().title() + ')'
			poke = poke[1].split('/type/')
			poketypes = poke[1:]
			poke_type = ''
			for i in range(0,len(poketypes)):
				if i > 0:
					poke_type += '/'
				temp = poketypes[i].split('"')
				poke_type += temp[0].title()
			pokestats = poke[-1].split('<td class="num')
			pokestats[1] = pokestats[1].replace('-total">','')
			pokestats[1] = pokestats[1][:4]
			pokestats[1] = pokestats[1].replace('<','')
			for j in range(2,8):
				pokestats[j] = pokestats[j][2:]
				pokestats[j] = pokestats[j][:4]
				pokestats[j] = pokestats[j].replace('<','')
				pokestats[j] = pokestats[j].replace('/','')
				pokestats[j] = pokestats[j].replace('t','')
			self.all_data.append([])
			self.all_data[idx].append(poke_name)
			self.all_data[idx].append(poke_type)
			self.all_data[idx].append(pokestats[1:8])
			idx += 1
	
	def getWeaknesses(self):
		self.list_pokeweak = []
		mega = 0
		self.typelist = ['normal','fire','water','electric','grass','ice','fighting','poison',
					'ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy']
		temp = str(self.html2)
		tempData = temp.split('<span class="pokedex_number">')[1:]
		stats = -1
		for pokemon in tempData:
			for idx,pokemon_names in enumerate(self.all_data):
				if len(pokemon_names) > 3:
					continue
				pokemon_name = pokemon_names[0].replace('-',' ').replace('(','').replace(')','').strip().lower()
				if ' ' in pokemon_name:
					templist = pokemon_name.split(' ')
					correct_name = 1
					for name_part in templist:
						if 'pirouette' in name_part and 'piro' in pokemon.lower():
							continue
						if name_part not in pokemon.lower():
							correct_name = 0
							break
					if correct_name:
						stats = idx
						break
				else:
					if pokemon_name.strip().lower() in pokemon.lower():
						stats = idx
						break
			Defenses = [[],[],[],[],[],[]]
			superweak = pokemon.split("superweak")
			superweak = superweak[-1].split("weak")
			weak = superweak[-1].split("normal_col")
			normal = weak[-1].split("resistant")
			resistant = "".join(normal[1:]).split("super")
			superresistant = resistant[-1].split("immune")
			immune = superresistant[-1]
			superresistant = superresistant[0]
			resistant = resistant[0]
			normal = normal[0]
			weak = weak[0]
			superweak = superweak[0]
			abilitystr = ''
			for type in self.typelist:
				if type in superweak:
					Defenses[0].append(type.title())
				if type in weak:
					Defenses[1].append(type.title())
				if type in normal:
					Defenses[2].append(type.title())
				if type in resistant:
					Defenses[3].append(type.title())
				if type in superresistant:
					Defenses[4].append(type.title())
				if type in immune:
					if "With ability: " in immune and immune.index("With ability: ") < immune.index(type):
						ability = immune.split("With ability: '")
						ability = ability[-1].split("'")
						Defenses[5].append(type.title() + '*')
						abilitystr = ability[0]
					else:
						Defenses[5].append(type.title())
			if abilitystr != '':
				Defenses[5][-1] += '    (With ability: ' + abilitystr + ')'
			if stats != -1:
				self.all_data[stats].append(Defenses)
				stats = -1
	
	def FixWeakness(self,idx):
		Type1 = ''
		Type2 = ''
		if '/' in self.all_data[idx][1]:
			Dualtype = self.all_data[idx][1].split('/')
			Type1 = Dualtype[0].lower()
			Type2 = Dualtype[1].lower()
		else:
			Type1 = self.all_data[idx][1].lower()
		for i,val in enumerate(self.all_data):
			if i == idx or len(val) == 3:
				continue
			else:
				if Type1 in val[1].lower() and Type2 in val[1].lower():
					Defenses_str = str(val[3])
					if 'With ability:' in Defenses_str:
						Defenses_0 = Defenses_str.split('(')
						Defenses_1 = Defenses_str.split(')')
						Defenses_str = Defenses_0[0] + Defenses_1[1]
						Defenses_str = Defenses_str.replace(' ','')
						Defenses = ast.literal_eval(Defenses_str)
						for val in Defenses[5]:
							if '*' in val:
								Defenses[5].remove(val)
						self.all_data[idx].append(Defenses)
					else:
						self.all_data[idx].append(val[3])