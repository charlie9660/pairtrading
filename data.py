from config import *
from api_init import *

class data(api_init):
	def __init__(self):
		super(data,self).__init__()

	def get_data(self,sym,period,limit):

		barset = None
		while (barset == None):
			try:
				barset = self.api.get_barset(sym, period, limit)
			except:
				print('Unable to retrieve data!')
				continue
		return barset.df