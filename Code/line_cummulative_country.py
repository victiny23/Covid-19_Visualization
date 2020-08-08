import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

# active cases
df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']

# China Cases, or any other country
china_df = df[df['Country'] == 'China'].groupby(['Date']).sum()

fig = china_df[['Confirmed','Recovered','Deaths','Active']].\
    plot(figsize=(12, 8), linewidth=2)
fig.set_xlabel('Date')
fig.set_ylabel('# of Cases')
fig.set_title('Covid-19 Cases in China')
plt.show()