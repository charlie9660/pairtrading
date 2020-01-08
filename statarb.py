import statsmodels.tsa.stattools as ts
from statsmodels.tsa.stattools import coint
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import pandas as pd
from utility import *

def get_conint_params(ts1,ts2): 

	if len(ts1) != len(ts2):
		return False
	else:
		df = pd.DataFrame([])

	df['ts_1'] = ts1
	df['ts_2'] = ts2

	# Calculate optimal hedge ratio "beta"
	res = smf.ols(formula='ts_2~ts_1', data = df).fit()
	beta_hr = res.params['ts_1']

    # Calculate the residuals of the linear combination
	df["res"] = df["ts_2"] - beta_hr*df["ts_1"]

     # Calculate and output the CADF test on the residuals
	df["res"].dropna(inplace=True)

	#compute 21-minute rolling residual
	res_norm = zscore(df['res'], 21)
	cadf = ts.adfuller(df["res"])

	mu = 0
	std = 0
	if cadf[0] < cadf[4]['10%']:#cadf[1] <= 0.1 or
		mu = df['res'].mean()
		std = df['res'].std()
		plt.plot(res_norm)
		plt.show()
	else:
		beta_hr = 0
        #pprint.pprint(cadf)
        #plot_residuals(df,s,e)

    #print mu,std,beta_hr
	return mu,std,beta_hr



def get_conint_params_2(ts1,ts2,window=30): 

	if len(ts1) != len(ts2):
		return False
	else:
		df = pd.DataFrame([])

	df['ts_1'] = ts1
	df['ts_2'] = ts2
	# Calculate optimal hedge ratio "beta"
	df = df.fillna(method ='ffill').dropna()
	df['ratio']  = [y/x for x,y in zip(ts1,ts2)]

	score, pvalue, _ = coint(ts1,ts2)
	#compute 21-minute rolling residual
	res_norm = zscore(df['ratio'], window).rolling(5).median()
	print("P: " + str(pvalue))
	#if pvalue < 0.3:#cadf[1] <= 0.1 or
	plt.plot(res_norm)
	plt.show()
	plt.plot(df['ratio'])
	plt.show()
	return pvalue

def signal_2(ts1,ts2,window=30):
	df = pd.DataFrame([])
	df['ts_1'] = ts1
	df['ts_2'] = ts2
	df = df.fillna(method ='ffill')
	df['ratio']  = [y/x for x,y in zip(ts1,ts2)] 
	z = zscore(df['ratio'], window).rolling(5).median()
	return z[-1]