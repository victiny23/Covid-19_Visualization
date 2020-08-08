import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

# active cases
df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']

# Worldwide Cases
worldwide_df = df.groupby(['Date']).sum()

w = worldwide_df.plot(figsize=(12, 8), linewidth=2)
w.set_xlabel('Date')
w.set_ylabel('# of Cases')
w.title.set_text('Worldwide Covid-19 Insights')
plt.tight_layout()
plt.show()