import os,wx

class Pokemon:
	def __init__(self):
		self.name = ''
		self.type = ''
		self.stats = []
		self.weaknesses = []
		self.image = wx.Bitmap('Images/0.png',wx.BITMAP_TYPE_PNG)
	
	def get(self):
		data = [self.name,self.type]
		data.extend(self.stats)
		return data
	
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