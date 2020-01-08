
from data import *
from trade import *
from statarb import *
from utility import *
from screener import *
import time
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

def main(tickers,window=500,z_window=20,interval=900):
	scr = screener()
	d = data()
	t = trade()
	count = 0
	l = 0
	s = 0

	sig = 0
	sig_prev = 0

	while (1==1):
		
		#re-calibrate position every certain period of time
		if (count == 0 or count > interval) and s + l == 0:
			df = scr.load_data(tickers,window)
			t1,t2,c = scr.select_pair(df)
			print("Best pair is: ",t1,t2)        
			print('Compute new co-integration parameters!')

			ts1 = d.get_data(t1,'minute',window)[t1]['close']
			ts2 = d.get_data(t2,'minute',window)[t2]['close']

			#get_conint_params_2(ts1.values,ts2.values,z_window)
			ts1_pos = round(500000 / ts1.values[-1]) 
			ts2_pos = round(ts1_pos * ts1.values[-1] / ts2.values[-1])
			print('Allocate ',str(ts1_pos),'in ',t1,' and ',str(ts2_pos),' in ',t2)
			count = 0

		if c < 0.2:
			ts1 = d.get_data(t1,'minute',window)[t1]['close']
			ts2 = d.get_data(t2,'minute',window)[t2]['close']
			#sig = signal(a,b,c,ts1,ts2)
			sig = signal_2(ts1,ts2,z_window)
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			print("Current Time:", current_time,' sig_prev:',sig_prev,' sig:',sig)
			if (sig_prev < -2.5 and sig > -2.5 and sig < -0.5 and l == 0) or (sig_prev > 0.5 and sig < 0.5 and s == 1):
				l = 1
				if s == 1:
					print('Close Activated')
					s += 1
				else:
					print('Long ',t2,'SHORT ', t1)
					t.trade(t2, ts2_pos, 'buy', 'market', 'gtc')
					t.trade(t1, ts1_pos, 'sell', 'market', 'gtc')

			elif sig_prev <0.5 and sig < 0.5 and s == 2:
				l =0
				s = 0
				print('Long ',t2,'SHORT ', t1)
				t.trade(t2, ts2_pos, 'buy', 'market', 'gtc')
				t.trade(t1, ts1_pos, 'sell', 'market', 'gtc')

			elif (sig_prev < -0.5 and sig > -0.5 and l ==1) or (sig_prev > 2.5 and sig < 2.5 and sig > 0.5 and s == 0):
				s = 1
				if l== 1:
					print('Close Activated')
					l += 1
				else:
					print('Short ',t2,'Long ', t1)
					t.trade(t2, ts2_pos, 'sell', 'market', 'gtc')
					t.trade(t1, ts1_pos, 'buy', 'market', 'gtc')

			elif sig_prev >-0.5 and sig > -0.5 and l ==2:
				l =0
				s = 0
				print('Short ',t2,'Long ', t1)
				t.trade(t2, ts2_pos, 'sell', 'market', 'gtc')
				t.trade(t1, ts1_pos, 'buy', 'market', 'gtc')

		else:
			print('No Cointegration detected! ',c)
			count = 0

		sig_prev = sig
		time.sleep(2)
		count += 1

if __name__ == "__main__":
	tickers = ['GOOG','AMZN','TSLA','FB','GM','DIS','FIT','NFLX']
	main(tickers=tickers,window=500,z_window=10,interval=300)