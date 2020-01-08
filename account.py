from config import * 
from api_init import *

class account(api_init):
	def __init__(self):
		super(account,self).__init__()

	def get_account(self):
		account = self.api.get_account()
		if account.trading_blocked:
			print('Account is restricted from trading')
			return None
		return account



