import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib.dates as mdates
# %matplotlib inline --> This is need in IPython
plt.style.use('fivethirtyeight')
# matplotlib.use('Qt5Agg')

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']
# print(df.head())


# Worldwide Cases
worldwide_df = df.groupby(['Date']).sum()
# print(worldwide_df.head())

"""
w = worldwide_df.plot(figsize=(12, 8), linewidth=2)
w.set_xlabel('Date')
w.set_ylabel('# of Cases')
w.title.set_text('Worldwide Covid-19 Insights')
plt.tight_layout()
plt.show()
"""

us_df = df[df['Country'] == 'US'].groupby(['Date']).sum()
china_df = df[df['Country'] == 'China'].groupby(['Date']).sum()

""" China """
fig = china_df[['Confirmed','Recovered','Deaths','Active']].\
    plot(figsize=(12, 8), linewidth=2)
fig.set_xlabel('Date')
fig.set_ylabel('# of Cases')
fig.set_title('Covid-19 Cases in China')

""" Worldwide vs US total
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
"""


""" get a list of default colors """
color_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
""" get the names of the columns """
column_list = list(worldwide_df.columns)
""" loop through the columns to plot """

""" Worldwide vs US Confirmed, Recovered, Deaths
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
"""



""" Top 10 countries with the most cases"""
total_country_df = df.groupby(['Country']).sum()
total_country_df = total_country_df.\
        sort_values([ 'Confirmed'], ascending=[0])
total_country_top10 = list(total_country_df.index[0:10])
fig = plt.figure(figsize=(15, 5))
time_stamps = ['Feb','Mar','Apr','May','Jun','Jul','Aug']
for i in range(3):
    ax = fig.add_subplot(1, 3, i+1)
    country_df = df[df['Country'] == total_country_top10[i]].groupby(['Date']).sum()
    ax.plot(country_df.iloc[:, :3], #label= column_list[i],
            linestyle='solid', alpha=0.6)
    if i < 1:
        ax.legend(list(worldwide_df.columns))
    ax.set_xlabel('Date')
    ax.set_ylabel('# of Cases')
    ax.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
    ax.set_ylim(-.1e6, 5e6)
    ax.title.set_text(str(total_country_top10[i]))
plt.suptitle('Countries with the most cases', fontsize=25)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

