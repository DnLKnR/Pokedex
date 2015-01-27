#Pokemon Types

import urllib
import os.path
import wx
import ast
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

##website: pokemondb.net

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.LC_NO_HEADER, size=(363,120))
        ListCtrlAutoWidthMixin.__init__(self)

class Pokedex:
	def __init__(self):
		self.pokemon = []
		self.unknown_init()
		
	def unknown_init(self):
		self.unknown = Pokemon()
		self.unknown.set_name('???')
		self.unknown.set_type('???')
		self.unknown.set_stats(['???','???','???',
								'???','???','???',
								'???'])
		self.unknown.set_weaknesses([['???'],['???'],
									 ['???'],['???'],
									 ['???'],['???']])
		self.unknown.set_image()
		
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
	
class Pokemon:
	def __init__(self):
		self.name = ''
		self.type = ''
		self.stats = []
		self.weaknesses = []
		self.image = wx.Bitmap('Images/0.png',wx.BITMAP_TYPE_PNG)
	
	def set_name(self,name):
		self.name = name
		
	def set_type(self,type):
		self.type = type
		
	def set_stats(self,stats):
		self.stats = stats
		
	def set_weaknesses(self,weaknesses):
		self.weaknesses = weaknesses
		
	def set_image(self):
		file_str = 'Images/' + self.get_name().lower() + '.png'
		if os.path.isfile(file_str):
			self.image = wx.Bitmap(file_str, wx.BITMAP_TYPE_PNG)

	def set_index(self, index):
		self.index = index
	
	def get_image(self):
		return self.image
	
	def get_name(self):
		return self.name
		
	def get_type(self):
		return self.type
		
	def get_stats(self):
		return self.stats
	
	def get_weaknesses(self):
		return self.weaknesses
		
	def get_quad(self):
		return ', '.join(self.weaknesses[0])
		
	def get_double(self):
		return ', '.join(self.weaknesses[1])
		
	def get_normal(self):
		return ', '.join(self.weaknesses[2])
		
	def get_half(self):
		return ', '.join(self.weaknesses[3])
		
	def get_fourth(self):
		return ', '.join(self.weaknesses[4])
		
	def get_immune(self):
		return ', '.join(self.weaknesses[5])
		
	def get_total(self):
		return self.stats[0]
		
	def get_hp(self):
		return self.stats[1]
		
	def get_atk(self):
		return self.stats[2]
		
	def get_def(self):
		return self.stats[3]
		
	def get_spatk(self):
		return self.stats[4]
		
	def get_spdef(self):
		return self.stats[5]
		
	def get_spd(self):
		return self.stats[6]
	
	def get_index(self):
		return self.index
		
class Window(wx.Frame):
	def __init__(self,parent,id,title):
		wx.Frame.__init__(self,parent,style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
		self.list_pokeweak = []
		file = open('pokedata.cfg','r')
		all_data_str = file.read()
		file.close()
		if all_data_str == '':
			file = open('pokedata.default.cfg','r')
			all_data_str = file.read()
			file.close()
			file = open('pokedata.cfg','w')
			file.write(all_data_str)
			file.close()
		self.all_data = ast.literal_eval(all_data_str)
		self.reset(self.all_data)
		self.typestrings = ["Quad","Double","Normal","Half","Fourth","Immune"]
		self.colors = ['#E8E8E8','#D0D0D0','#B8B8B8','#A0A0A0','#888888','#707070']
		self.icon = wx.Icon('Images/pokeball.ico',wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)
		self.SB1 = wx.StaticBox(self,-1,'Stats')
		self.SB1.SetBackgroundColour('white')
		self.CB = wx.ComboBox(self,-1,value='',choices=['Name','Type'],style=wx.CB_READONLY,size=(103,-1))
		self.CB.SetSelection(0)
		#create menubar
		self.menubar = wx.MenuBar()
		self.filemenu = wx.Menu()
		self.m_stayontop = self.filemenu.Append(wx.ID_ANY,'Stay on Top [Off]\tCtrl-S','')
		self.m_track = self.filemenu.Append(wx.ID_ANY,'Show Tracked\tCtrl-T','')
		self.m_rescrape = self.filemenu.Append(wx.ID_ANY,'Rescrape Html\tCtrl-R','')
		self.m_close = self.filemenu.Append(wx.ID_ANY, 'Close\tCtrl-Q','')
		self.menubar.Append(self.filemenu, 'File')
		self.Bind(wx.EVT_MENU, self.stay_on_top, self.m_stayontop)
		self.Bind(wx.EVT_MENU, self.toggle_track_mode, self.m_track)
		self.Bind(wx.EVT_MENU, self.rescrape, self.m_rescrape)
		self.Bind(wx.EVT_MENU, self.CloseWindow, self.m_close)
		#Creating list that will store all pokemon
		self.LC = wx.ListCtrl(self,-1,style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.LC2 = AutoWidthListCtrl(self)
		self.dc = wx.ClientDC(self.LC2)
		#Inserting columns into that list of pokemon
		self.LC.InsertColumn(0,'Pokemon',format=wx.LIST_FORMAT_LEFT,width=90)
		self.LC.InsertColumn(1,'Type',format=wx.LIST_FORMAT_CENTER,width=100)
		self.LC.InsertColumn(2,'Total',format=wx.LIST_FORMAT_CENTER,width=45)
		self.LC.InsertColumn(3,'HP',format=wx.LIST_FORMAT_CENTER,width=30)
		self.LC.InsertColumn(4,'Atk',format=wx.LIST_FORMAT_CENTER,width=30)
		self.LC.InsertColumn(5,'Def',format=wx.LIST_FORMAT_CENTER,width=30)
		self.LC.InsertColumn(6,'SpAtk',format=wx.LIST_FORMAT_CENTER,width=44)
		self.LC.InsertColumn(7,'SpDef',format=wx.LIST_FORMAT_CENTER,width=44)
		self.LC.InsertColumn(8,'Spd',format=wx.LIST_FORMAT_CENTER,width=35)
		self.LC2.InsertColumn(0,'Damage Taken [(2 ^ Row) * 1/4]',format=wx.LIST_FORMAT_RIGHT,width=355)
		
		#creating boxsizers
		mainbox = wx.BoxSizer(wx.VERTICAL)
		statsbox = wx.BoxSizer(wx.HORIZONTAL)
		imagebox = wx.StaticBoxSizer(self.SB1,wx.HORIZONTAL)
		defensebox = wx.BoxSizer(wx.HORIZONTAL)
		box = wx.BoxSizer(wx.VERTICAL)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		
		#creating initial image for imagebox
		self.image = wx.StaticBitmap(self, -1, wx.Bitmap('Images/0.png',wx.BITMAP_TYPE_PNG))
		self.input = wx.TextCtrl(self,value='',size=(270,-1))
		
		self.SetBackgroundColour('pink')
		
		#Adding text entry and combobox to a hbox then adding it the box
		hbox.Add(self.input,wx.EXPAND | wx.ALIGN_LEFT)
		hbox.Add(self.CB,wx.ALIGN_CENTER)
		box.Add(hbox,flag = wx.ALL)
		
		#Adding list that will store all pokemon
		box.Add(self.LC,flag = wx.ALL | wx.EXPAND)
		
		#Adding image area to imagebox
		imagebox.Add(self.image,flag = wx.ALIGN_CENTER | wx.ALL)
		
		defensebox.Add(self.LC2,flag = wx.ALIGN_CENTER | wx.EXPAND)
		#Adding image to boxsizer
		statsbox.Add(imagebox,flag = wx.ALIGN_CENTER | wx.ALL)
		
		#Adding boxsizer to mainbox
		box.Add(statsbox,flag = wx.ALIGN_CENTER | wx.EXPAND)
		
		self.SetMenuBar(self.menubar)
		
		statsbox.Add(defensebox,flag = wx.ALIGN_CENTER | wx.EXPAND)
		mainbox.Add(box,flag = wx.ALL | wx.EXPAND)
		
		self.Bind(wx.EVT_TEXT,self.search,self.input)
		self.Bind(wx.EVT_LIST_ITEM_FOCUSED,self.set_information,self.LC)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.track,self.LC)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.track,self.LC)
		self.Bind(wx.EVT_TEXT_ENTER,self.track,self.input)
		
		self.SetSizer(mainbox)
		mainbox.Fit(self)
		self.refresh('')
	
	def reset(self,array):
		self.track_mode = 0
		self.Tracked = Pokedex()
		self.Pokedex = Pokedex()
		self.Pokedex.add_all(array)
		
	def stay_on_top(self,event):
		if self.ToggleWindowStyle(flag = wx.STAY_ON_TOP):
			self.m_stayontop.SetItemLabel('Stay on Top [On]\tCtrl-S')
		else:
			self.m_stayontop.SetItemLabel('Stay on Top [Off]\tCtrl-S')
	
	def track(self,event):
		if self.LC.GetItemCount():
			index = self.LC.GetFocusedItem()
			if index == -1: index = 0
			ListItem = self.LC.GetItem(index,0)
			Name = ListItem.GetText()
			if self.track_mode:
				self.Tracked.remove(Name)
				filter = self.input.GetValue().strip().lower()
				self.refresh(filter)
			else:
				pokemon = self.Pokedex.get(Name)
				self.Tracked.add(pokemon)
		
	def toggle_track_mode(self,event):
		if self.track_mode:
			self.m_track.SetItemLabel('Show Tracked\tCtrl-T')
			self.track_mode = 0
		else:
			self.m_track.SetItemLabel('Show All\tCtrl-T')
			self.track_mode = 1
		self.input.SetValue('')
		self.refresh('')
		
	def refresh(self,filter):
		self.LC.DeleteAllItems()
		selection = self.CB.GetSelection()
		if self.track_mode:
			if selection == 0:
				subset = self.Tracked.name_filter(filter)
			else:
				subset = self.Tracked.type_filter(filter)
		else:
			if selection == 0:
				subset = self.Pokedex.name_filter(filter)
			else:
				subset = self.Pokedex.type_filter(filter)
		if len(subset) < 2 and subset[0].get_name() == '???':
			pass
		else:
			for index,pokemon in enumerate(subset):
				self.LC.InsertStringItem(index,pokemon.get_name())
				self.LC.SetStringItem(index,1,pokemon.get_type())
				self.LC.SetStringItem(index,2,pokemon.get_total())
				self.LC.SetStringItem(index,3,pokemon.get_hp())
				self.LC.SetStringItem(index,4,pokemon.get_atk())
				self.LC.SetStringItem(index,5,pokemon.get_def())
				self.LC.SetStringItem(index,6,pokemon.get_spatk())
				self.LC.SetStringItem(index,7,pokemon.get_spdef())
				self.LC.SetStringItem(index,8,pokemon.get_spd())
				if index % 2 == 0:
					self.LC.SetItemBackgroundColour(index,"pink")
		self.SB1.SetLabel(subset[0].get_name())
		self.set_image(subset[0].get_image())
		self.set_weaknesses(subset[0])
		self.LC.Select(0,on=1)
	
			
	def set_information(self,event):
		self.LC2.DeleteAllItems()
		ListItem = self.LC.GetItem(self.LC.GetFocusedItem(),0)
		Name = ListItem.GetText()
		pokemon = self.Pokedex.get(Name)
		self.set_weaknesses(pokemon)
		self.SB1.SetLabel(pokemon.get_name())
		# self.LC2.resizeLastColumn(-1)
		self.set_image(pokemon.get_image())
	
	def set_weaknesses(self,pokemon):
		self.LC2.DeleteAllItems()
		self.LC2.InsertStringItem(0,pokemon.get_quad())
		self.LC2.SetItemBackgroundColour(0,self.colors[0])
		self.LC2.InsertStringItem(1,pokemon.get_double())
		self.LC2.SetItemBackgroundColour(1,self.colors[1])
		self.LC2.InsertStringItem(2,pokemon.get_normal())
		self.LC2.SetItemBackgroundColour(2,self.colors[2])
		self.LC2.InsertStringItem(3,pokemon.get_half())
		self.LC2.SetItemBackgroundColour(3,self.colors[3])
		self.LC2.InsertStringItem(4,pokemon.get_fourth())
		self.LC2.SetItemBackgroundColour(4,self.colors[4])
		self.LC2.InsertStringItem(5,pokemon.get_immune())
		self.LC2.SetItemBackgroundColour(5,self.colors[5])
		self.LC2.resizeLastColumn(-1)
		
	def set_image(self,image):
		self.image.SetBitmap(image)
	
	def search(self,event):
		filter = self.input.GetValue().strip().lower()
		self.refresh(filter)
	
	def rescrape(self,event):
		self.Hide()
		self.mySplash = wx.SplashScreen(app.myBitmap, wx.SPLASH_NO_TIMEOUT | wx.SPLASH_CENTRE_ON_PARENT, -1, None)
		self.mySplash.Show()
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
		self.refresh('')
		self.mySplash.Destroy()
		self.Show()
		
	def CloseWindow(self,event):
		self.Destroy()

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

app = wx.App()
app.myBitmap = wx.Bitmap('Images/Pokemon_Logo.png',wx.BITMAP_TYPE_PNG)
app.mySplash = wx.SplashScreen(app.myBitmap, wx.SPLASH_NO_TIMEOUT | wx.SPLASH_CENTER_ON_SCREEN, -1, None)
app.mySplash.Show()
app.Window = Window(None,-1,"Pokedex")
app.Window.SetTitle('Pokedex')
app.Window.Show()
app.mySplash.Destroy()
app.MainLoop()
