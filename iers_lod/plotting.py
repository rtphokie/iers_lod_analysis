from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import datetime
from scipy.signal import savgol_filter

import os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def plotit(df, column_of_interest='Bull. A LOD', label='length of day variance (milliseconds)',
           start=datetime.datetime(1973, 1, 2), trend=True, filename='result.png'):
    df = df[df.index >= start]
    plt.figure(figsize=(16, 9), dpi=300)
    window = 999
    order = 3
    df[column_of_interest].plot(style='grey', label=label)
    if trend:
        df['trend'] = savgol_filter(df[column_of_interest], window, order)
        df['trend'].plot(style='b-', label=label, lw=3)
    plt.axis('off')
    # plt.show()
    plt.savefig(filename)
