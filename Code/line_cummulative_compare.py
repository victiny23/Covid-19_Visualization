import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

# active cases
df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']

# Worldwide Cases
worldwide_df = df.groupby(['Date']).sum()
# US Cases
us_df = df[df['Country'] == 'US'].groupby(['Date']).sum()

"""
Worldwide vs US or any other country,
or comparision among countries
"""
# Compare confirmed cases only
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)  # 1 x 1 grid, 1st subplot
ax.plot(worldwide_df[['Confirmed']], alpha=0.8, label='Worldwide')
ax.plot(us_df[['Confirmed']], alpha=0.8, label='United States')
ax.set_xlabel('Date')
ax.set_ylabel('# of Cases')
ax.title.set_text('Worldwide vs. United States Covid-19 Total Cases')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()


""" get a list of default colors """
color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
""" get the names of the columns """
column_list = list(worldwide_df.columns)
""" loop through the columns to plot """

# Compare confirmed, recovered, and deaths
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)  # 1 x 1 grid, 1st subplot
for i in range(3):
    ax.plot(worldwide_df.iloc[:, i], linewidth=3,
            label='Worldwide'+' '+column_list[i],
            linestyle='solid', alpha=0.8,
            color=color_list[i])
    ax.plot(us_df.iloc[:, i], linewidth=3,
            label='US' + ' ' + column_list[i],
            linestyle='dashed', alpha=0.8,
            color=color_list[i])
ax.set_xlabel('Date')
ax.set_ylabel('# of Cases')
ax.title.set_text('Worldwide vs. United States Covid-19 Cases')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

