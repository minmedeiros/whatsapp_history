import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

#Set file name
file = 'Conversation'

# Read whatsapp history file
data = pd.read_csv(file+'.txt', sep='\t', header = None)
data.columns = ['text']

# Init future columns for dataframe
date = []
time = []
text = []

# Go through history data
for idx in data.index:
    # Select lines that start with the date (sometimes messages are split into more than one line)
    if (len(data['text'][idx])>10) and (str(data['text'][idx])[2] == '/') and (str(data['text'][idx])[0] == '0' or str(data['text'][idx])[0] == '1' or str(data['text'][idx])[0] == '2'):
        # Split full text from DATE - TIME - TEXT to separate variables
        date.append(str(data['text'][idx])[0:10])
        time.append(str(data['text'][idx])[11:16])
        text.append(str(data['text'][idx])[17:])

print(len(date))
print(len(time))

# Init frequency of message as one per line
freq = np.ones(len(date))

# Set conversation dataframe with date, time, text and frequency data and columns
conversation = pd.DataFrame(data = [date, time, text, freq]).T
conversation.columns=['date','hour','text','frequency']
print(conversation.date)

# Group conversation by day
conversation.date = pd.to_datetime(conversation.date, errors='coerce', dayfirst=True, format='%d/%m/%Y')
conversation_day = conversation.groupby(pd.Grouper(key='date', freq='1D')).sum()
conversation_day.index = conversation_day.index.strftime('%B')

# Group conversation by month
conversation_month = conversation.groupby(pd.Grouper(key='date', freq='1M')).sum()
conversation_month.index = conversation_month.index.strftime('%B')

# Plot images
conversation_day.plot()
plt.savefig(file+'_daily.png')
plt.show()

conversation_month.plot()
plt.savefig(file+'_monthly.png')
plt.show()
