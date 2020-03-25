import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import numpy as np

data = pd.read_csv("Conversation.txt",sep='\t')
data.columns = ['text']
date = []
time = []
text = []
times = []
dates = []

for idx in data.index:
    if (len(data['text'][idx])>10) and (str(data['text'][idx])[2] == '/') and (str(data['text'][idx])[0] == '0' or str(data['text'][idx])[0] == '1' or str(data['text'][idx])[0] == '2'):
        date.append(str(data['text'][idx])[0:10])
        time.append(str(data['text'][idx])[11:16])
        text.append(str(data['text'][idx])[17:])

freq = np.ones(len(date))
conversation = pd.DataFrame(data = [date, time, text, freq]).T
conversation.columns=['date','hour','text','frequency']

conversation.date = pd.to_datetime(conversation.date,dayfirst=True)
conversation_day = conversation.groupby(pd.Grouper(key='date', freq='1D')).sum() # groupby each 1 month
conversation_day.index = conversation_day.index.strftime('%B')

conversation_month = conversation.groupby(pd.Grouper(key='date', freq='1M')).sum() # groupby each 1 month
conversation_month.index = conversation_month.index.strftime('%B')

conversation_day.plot()
plt.show()

conversation_month.plot()
plt.show()
