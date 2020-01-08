from config import *
from api_init import *

class trade(api_init):

	def __init__(self):
		super(trade,self).__init__()

	def trade(self,symbol, qty, side, type, tf):
		r = self.api.submit_order(symbol = symbol,
			qty = qty,
			side = side,
			type = type,
			time_in_force = tf)
		return r

	def get_positions(self):
		orders = self.api.list_orders(status='open')
		return orders

	def cancel_orders(self,id):
		return self.api.cancel_order(id)

