import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
# Worldwide Cases
worldwide_df = df.groupby(['Date']).sum()
# Worldwide Daily Cases and Deaths
worldwide_df['Daily Confirmed'] = worldwide_df['Confirmed'].sub(worldwide_df['Confirmed'].shift())
worldwide_df['Daily Deaths'] = worldwide_df['Deaths'].sub(worldwide_df['Deaths'].shift())

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.bar(worldwide_df.index, worldwide_df['Daily Confirmed'], color='b',
       label='Worldwide Daily Confirmed')
ax.bar(worldwide_df.index, worldwide_df['Daily Deaths'], color='r',
       label='Worldwide Daily Deaths')
ax.set_xlabel('Date')
ax.set_ylabel('# of Cases')
ax.set_title('Worldwide Covid-19 Daily Cases')
plt.legend(loc='upper left')
plt.show()
