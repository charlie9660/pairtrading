from config import *
from api_init import *

class asset(api_init):

	def __init__(self):
		super(asset,self).__init__()

	def check_asset(self,sym):
		try:
			asset = self.api.get_asset(sym)
			if asset.tradable:
			    return True
		except:
			return False