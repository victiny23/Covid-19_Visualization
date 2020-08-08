import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
# US cases, or any other country
us_df = df[df['Country'] == 'US'].groupby(['Date']).sum()
# US Daily Cases and Deaths
us_df['Daily Confirmed'] = us_df['Confirmed'].sub(us_df['Confirmed'].shift())
us_df['Daily Deaths'] = us_df['Deaths'].sub(us_df['Deaths'].shift())

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.bar(us_df.index, us_df['Daily Confirmed'], color='b',
       label='US Daily Confirmed')
ax.bar(us_df.index, us_df['Daily Deaths'], color='r',
       label='US Daily Deaths')
ax.set_xlabel('Date')
ax.set_ylabel('# of Cases')
ax.set_title('US Covid-19 Daily Cases')
plt.legend(loc='upper left')
plt.show()
