import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
# active cases
df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']
# Worldwide Cases
worldwide_df = df.groupby(['Date']).sum()
time_stamps = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']

us_df = df[df['Country'] == 'US'].groupby(['Date']).sum()

# calculate percentage
worldwide_df['RecoveredPct'] = worldwide_df['Recovered'] / worldwide_df['Confirmed'] * 100
worldwide_df['DeathsPct'] = worldwide_df['Deaths'] / worldwide_df['Confirmed'] * 100
worldwide_df['ActivePct'] = worldwide_df['Active'] / worldwide_df['Confirmed'] * 100

us_df['RecoveredPct'] = us_df['Recovered'] / us_df['Confirmed'] * 100
us_df['DeathsPct'] = us_df['Deaths'] / us_df['Confirmed'] * 100
us_df['ActivePct'] = us_df['Active'] / us_df['Confirmed'] * 100

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(2, 2, 1)
ax.plot([], [], color='m', label='Deaths', linewidth=5)
ax.plot([], [], color='c', label='Active', linewidth=5)
ax.plot([], [], color='r', label='Recovered', linewidth=5)
ax.stackplot(worldwide_df.index, worldwide_df['Deaths'],
             worldwide_df['Active'], worldwide_df['Recovered'],
             colors=['m', 'c', 'r'])
ax.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
ax.set_xlabel('Date')
ax.set_ylabel('# of Cases')
ax.title.set_text('Worldwide')
ax.legend(['Deaths', 'Active', 'Recovered'], loc='upper left')

ax = fig.add_subplot(2, 2, 2)
ax.grid(False)
ax.plot([], [], color='m', label='Deaths', linewidth=5)
ax.plot([], [], color='c', label='Active', linewidth=5)
ax.plot([], [], color='r', label='Recovered', linewidth=5)
ax.stackplot(worldwide_df.index, worldwide_df['DeathsPct'],
             worldwide_df['ActivePct'], worldwide_df['RecoveredPct'],
             colors=['m', 'c', 'r'])
ax.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
ax.set_xlabel('Date')
ax.set_ylabel('Percentage (%)')
ax.title.set_text('Worldwide (%)')

ax = fig.add_subplot(2, 2, 3)
ax.plot([], [], color='m', label='Deaths', linewidth=5)
ax.plot([], [], color='c', label='Active', linewidth=5)
ax.plot([], [], color='r', label='Recovered', linewidth=5)
ax.stackplot(us_df.index, us_df['Deaths'],
             us_df['Active'], us_df['Recovered'],
             colors=['m', 'c', 'r'])
ax.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
ax.set_xlabel('Date')
ax.set_ylabel('# of Cases')
ax.title.set_text('US')
ax.set_ylim(0, 2e7)

ax = fig.add_subplot(2, 2, 4)
ax.grid(False)
ax.plot([], [], color='m', label='Deaths', linewidth=5)
ax.plot([], [], color='c', label='Active', linewidth=5)
ax.plot([], [], color='r', label='Recovered', linewidth=5)
ax.stackplot(us_df.index, us_df['DeathsPct'],
             us_df['ActivePct'], us_df['RecoveredPct'],
             colors=['m', 'c', 'r'])
ax.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
ax.set_xlabel('Date')
ax.set_ylabel('Percentage (%)')
ax.title.set_text('US (%)')

plt.suptitle('Covid-19 Tracking', fontsize=25)
plt.tight_layout()
plt.show()

