#Pokemon Types
from pokelist import PokeList
from scrape import Scrape
import os.path, wx, ast
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
#website: pokemondb.net

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.LC_NO_HEADER, size=(363,120))
        ListCtrlAutoWidthMixin.__init__(self)
	
class Pokedex(wx.Frame):
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
		self.settings = wx.Menu()
		self.m_stayontop = self.settings.Append(wx.ID_ANY,'Stay on Top [Off]\tCtrl-S','')
		self.m_resize = self.settings.Append(wx.ID_ANY,'Resizable [Off]\tCtrl-E','')
		self.filemenu.Append(wx.ID_ANY,'Options...',self.settings)
		self.m_track = self.filemenu.Append(wx.ID_ANY,'Show Tracked\tCtrl-T','')
		self.m_rescrape = self.filemenu.Append(wx.ID_ANY,'Rescrape Html\tCtrl-R','')
		self.m_close = self.filemenu.Append(wx.ID_ANY, 'Close\tCtrl-Q','')
		self.menubar.Append(self.filemenu, 'File')
		self.Bind(wx.EVT_MENU, self.stay_on_top, self.m_stayontop)
		self.Bind(wx.EVT_MENU, self.toggle_track_mode, self.m_track)
		self.Bind(wx.EVT_MENU, self.rescrape, self.m_rescrape)
		self.Bind(wx.EVT_MENU, self.on_close, self.m_close)
		#Creating list that will store all pokemon
		self.LC = wx.ListCtrl(self,-1,style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		#Creating list for weaknesses
		self.LC2 = AutoWidthListCtrl(self)
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
		
		#Bind Events to search bar
		self.Bind(wx.EVT_TEXT,self.search,self.input)
		self.Bind(wx.EVT_CHAR_HOOK,self.on_keyboard_search,self.input)
		
		#Bind Events to Search Combobox
		self.Bind(wx.EVT_COMBOBOX,self.search,self.CB)
		self.Bind(wx.EVT_CHAR_HOOK,self.on_keyboard_combobox,self.CB)
		
		#Bind Events to Pokemon ListCtrl
		self.Bind(wx.EVT_LIST_ITEM_FOCUSED,self.set_information,self.LC)
		self.Bind(wx.EVT_LIST_KEY_DOWN,self.on_keyboard_list,self.LC)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.track,self.LC)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.track,self.LC)
		self.Bind(wx.EVT_TEXT_ENTER,self.track,self.input)
		
		#Resize and Refresh the list
		self.SetSizer(mainbox)
		mainbox.Fit(self)
		self.refresh('')
	
	def on_keyboard_search(self,event):
		if event.GetKeyCode() == wx.WXK_DOWN:
			if self.LC.GetItemCount():
				self.LC.Focus(0)
				self.LC.SetFocus()
		elif event.GetKeyCode() == wx.WXK_UP:
			#Do Nothing
			pass
		elif event.GetKeyCode() == wx.WXK_TAB:
			self.CB.SetFocus()
		else:
			#Handle event default
			event.Skip()
	
	def on_keyboard_list(self,event):
		if event.GetKeyCode() == wx.WXK_UP:
			index = self.LC.GetFocusedItem()
			if index == 0:
				self.input.SetFocus()
		elif event.GetKeyCode() == wx.WXK_TAB:
			self.input.SetFocus()
		else:
			#Handle event default
			event.Skip()
	
	def on_keyboard_combobox(self,event):
		if event.GetKeyCode() == wx.WXK_TAB:
			self.input.SetFocus()
		else:
			#Handle Event default
			event.Skip()
	
	def on_close(self,event):
		self.Destroy()
	
	def reset(self,array):
		self.p_filter = ''
		self.track_mode = 0
		self.Tracked = PokeList()
		self.Pokedex = PokeList()
		self.Scrape = Scrape()
		self.Pokedex.add_all(array)
		
	def stay_on_top(self,event):
		if self.ToggleWindowStyle(flag = wx.STAY_ON_TOP):
			self.m_stayontop.SetItemLabel('Stay on Top [On]\tCtrl-S')
		else:
			self.m_stayontop.SetItemLabel('Stay on Top [Off]\tCtrl-S')
	
	def resizable(self,event):
		if self.ToggleWindowStyle(flag = wx.RESIZE_BORDER | wx.MAXIMIZE_BOX):
			self.m_resize.SetItemLabel('Resizable [Off]\tCtrl-E')
		else:
			self.m_resize.SetItemLabel('Resizable [On]\tCtrl-E')
	
	def track(self,event):
		if self.LC.GetItemCount():
			index = self.LC.GetFocusedItem()
			if index == -1: 
				index = 0
			ListItem = self.LC.GetItem(index,0)
			Name = ListItem.GetText()
			if self.track_mode:
				self.Tracked.remove(Name)
				filter = self.input.GetValue().strip().lower()
				self.refresh(filter)
			else:
				pokemon = self.Pokedex.get(Name)
				self.Tracked.add(pokemon)
			if self.LC.GetItemCount() == 0:
				self.input.SetFocus()
		
	def toggle_track_mode(self,event):
		if self.track_mode:
			self.m_track.SetItemLabel('Show Tracked\tCtrl-T')
			self.track_mode = 0
		else:
			self.m_track.SetItemLabel('Show All\tCtrl-T')
			self.track_mode = 1
		self.input.SetValue('')
		self.refresh('')
	
	def set_item_color(self,index,color1,color2):
		if index % 2:
			self.LC.SetItemBackgroundColour(index,color1)
		else:
			self.LC.SetItemBackgroundColour(index,color2)
		
	def set_items(self,set):
		self.LC.DeleteAllItems()
		for index,pokemon in enumerate(set):
			self.append_item(pokemon)
			self.set_item_color(index,'pink','white')
			
	def add_items(self,set):
		column = self.CB.GetSelection()
		i,max_i = (0,self.LC.GetItemCount())
		j,max_j = (0,len(set))
		while True:
			if j == max_j: break
			elif i == max_i:
				self.insert_item(i,set[j])
				max_i += 1
			else:
				ListItem = self.LC.GetItem(i,column)
				ItemText = ListItem.GetText()
				if not set[j].get_name() == ItemText:
					self.insert_item(i,set[j])
					max_i += 1
			self.set_item_color(i,'pink','white')
			i,j = (i+1,j+1)
				
	def refresh(self,filter):
		if self.track_mode:
			if filter == '':
				subset = self.Tracked.get_all()
			elif self.CB.GetSelection():
				subset = self.Tracked.type_filter(filter)
			else:
				subset = self.Tracked.name_filter(filter)
		else:
			if filter == '':
				subset = self.Pokedex.get_all()
			elif self.CB.GetSelection():
				subset = self.Pokedex.type_filter(filter)
			else:
				subset = self.Pokedex.name_filter(filter)
		if subset[0].get_name() == '???':
			self.LC.DeleteAllItems()
		elif self.p_filter in filter:
			self.set_items(subset)
		else:
			self.add_items(subset)
		self.p_filter = filter
		self.SB1.SetLabel(subset[0].get_name())
		self.set_image(subset[0].get_image())
		self.set_weaknesses(subset[0])
		self.LC.Select(0,on=1)
	
	def insert_item(self, index, pokemon):
		self.LC.InsertItem(index,pokemon.get_name())
		self.LC.SetItem(index,1,pokemon.get_type())
		self.LC.SetItem(index,2,pokemon.get_total())
		self.LC.SetItem(index,3,pokemon.get_hp())
		self.LC.SetItem(index,4,pokemon.get_atk())
		self.LC.SetItem(index,5,pokemon.get_def())
		self.LC.SetItem(index,6,pokemon.get_spatk())
		self.LC.SetItem(index,7,pokemon.get_spdef())
		self.LC.SetItem(index,8,pokemon.get_spd())
	
	def append_item(self, pokemon):
		self.LC.Append(pokemon.get())
	
	def set_information(self,event):
		self.LC2.DeleteAllItems()
		ListItem = self.LC.GetItem(self.LC.GetFocusedItem(),0)
		Name = ListItem.GetText()
		pokemon = self.Pokedex.get(Name)
		self.set_weaknesses(pokemon)
		self.SB1.SetLabel(pokemon.get_name())
		self.set_image(pokemon.get_image())
	
	def set_weaknesses(self,pokemon):
		self.LC2.DeleteAllItems()
		self.LC2.InsertItem(0,pokemon.get_quad())
		self.LC2.SetItemBackgroundColour(0,self.colors[0])
		self.LC2.InsertItem(1,pokemon.get_double())
		self.LC2.SetItemBackgroundColour(1,self.colors[1])
		self.LC2.InsertItem(2,pokemon.get_normal())
		self.LC2.SetItemBackgroundColour(2,self.colors[2])
		self.LC2.InsertItem(3,pokemon.get_half())
		self.LC2.SetItemBackgroundColour(3,self.colors[3])
		self.LC2.InsertItem(4,pokemon.get_fourth())
		self.LC2.SetItemBackgroundColour(4,self.colors[4])
		self.LC2.InsertItem(5,pokemon.get_immune())
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
		self.all_data = self.Scrape.scrape()
		self.reset(self.all_data)
		self.refresh('')
		self.mySplash.Destroy()
		self.Show()

app = wx.App()
app.myBitmap = wx.Bitmap('Images/Pokemon_Logo.png',wx.BITMAP_TYPE_PNG)
# app.mySplash = wx.SplashScreen(app.myBitmap, wx.SPLASH_NO_TIMEOUT | wx.SPLASH_CENTER_ON_SCREEN, -1, None)
# app.mySplash.Show()
app.Pokedex = Pokedex(None,-1,"Pokedex")
app.Pokedex.SetTitle('Pokedex')
app.Pokedex.Show()
# app.mySplash.Destroy()
app.MainLoop()
