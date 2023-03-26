import pandas as pd

# read data from text file
value = pd.read_csv('vix.txt',sep='\t',header=None,names=['value'])
date = pd.read_csv('vix_date.txt',sep='\t',header=None,names=['date'])

# combine value and date DataFrames
df = pd.concat([date, value], axis=1)
df['date'] = pd.to_datetime(df['date'])

# calculate daily metrics
daily_open = df['value'].groupby(df['date'].dt.date).first()
daily_close = df['value'].groupby(df['date'].dt.date).last()
daily_volatility = df['value'].groupby(df['date'].dt.date).std()
daily_average = df['value'].groupby(df['date'].dt.date).mean()
daily_high = df['value'].groupby(df['date'].dt.date).max()
daily_low = df['value'].groupby(df['date'].dt.date).min()

# store daily metrics in a text file
with open('metrics.txt', 'w') as f:
    f.write('Open: {:.2f}\n'.format(daily_open[-1]))
    f.write('Close: {:.2f}\n'.format(daily_close[-1]))
    f.write('Volatility: {:.2f}\n'.format(daily_volatility[-1]))
    f.write('Average: {:.2f}\n'.format(daily_average[-1]))
    f.write('High: {:.2f}\n'.format(daily_high[-1]))
    f.write('Low: {:.2f}\n'.format(daily_low[-1]))
