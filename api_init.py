import alpaca_trade_api as tradeapi
from config import *

class api_init():

	def __init__(self):
		self.api =  tradeapi.REST(
		API_KEY,
		SECRET_KEY,
		BASE_URL
		)
