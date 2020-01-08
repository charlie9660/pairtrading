from config import *
from api_init import *
import pandas as pd
from data import *
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint

class screener(api_init):

	def __init__(self):
		super(screener,self).__init__()
		self.data = data()

	def load_data(self,syms,window):
		assets = pd.DataFrame([])
		for sym in syms:
			assets[sym] = self.data.get_data(sym,'minute',window)[sym]['close']

		return assets

	def select_pair(self,df):
		p_min = 100
		sym1 = ""
		sym2 = ""
		df = df.fillna(method ='ffill').dropna()
		for col1 in df.columns:
			for col2 in df.columns:
				score, pvalue, _ = coint(df[col1],df[col2])
				print(col1,col2,pvalue)
				if pvalue < p_min and pvalue != 0:
					p_min = pvalue
					sym1 = col1
					sym2 = col2
		print('Best P-value: ', str(p_min))
		return	sym1, sym2,p_min

	def plot_corr(self,df):
		# calculate the correlation matrix
		corr = df.corr()
		corr = corr[corr > 0.8]

		plt.figure(figsize=(len(df.columns)+1,len(df.columns)+1))
		# plot the heatmap
		sns.heatmap(corr, 
		        xticklabels=corr.columns,
		        yticklabels=corr.columns,
		        vmin = -1,
		        vmax = 1,
		        cmap ='coolwarm',
		        annot=True)
		plt.show()