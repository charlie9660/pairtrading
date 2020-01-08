import pandas as pd
import matplotlib.pyplot as plt

def twin_plot(df1,df2,df1_title,df2_title):

    common_index = df1.index.intersection(df2.index)
    df1 = df1.reindex(common_index)
    df2 = df2.reindex(common_index)

    fig, ax1 = plt.subplots()

    color = 'tab:green'
    ax1.set_xlabel('Date')
    ax1.set_ylabel(df1_title, color=color)
    ax1.plot(common_index, df1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.axhline(y=2, color='r', linestyle='-')
    plt.axhline(y=-2, color='r', linestyle='-')
    plt.xticks(rotation = 90)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(df2_title, color=color)  # we already handled the x-label with ax1
    ax2.plot(common_index, df2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

def zscore(x, window):
    r = x.rolling(window=window)
    m = r.mean().shift(1)
    s = r.std(ddof=0).shift(1)
    z = (x-m)/s
    return z