import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib.dates as mdates
from datetime import date, timedelta
# %matplotlib inline --> This is need in IPython
# plt.style.use('fivethirtyeight')
# matplotlib.use('Qt5Agg')

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']
# print(df.head())
time_stamps = ['Feb','Mar','Apr','May','Jun','Jul','Aug']

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

""" China 
fig = china_df[['Confirmed','Recovered','Deaths','Active']].\
    plot(figsize=(12, 8), linewidth=2)
fig.set_xlabel('Date')
fig.set_ylabel('# of Cases')
fig.set_title('Covid-19 Cases in China')
"""

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



""" Top 10 countries with the most cases
total_country_df = df.groupby(['Country']).sum()
total_country_df = total_country_df.\
        sort_values([ 'Confirmed'], ascending=[0])
total_country_top10 = list(total_country_df.index[0:10])
fig = plt.figure(figsize=(15, 5))
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
"""

""" US Daily Cases and Deaths
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
"""



""" China Daily Cases and Deaths
china_df['Daily Confirmed'] = china_df['Confirmed'].sub(china_df['Confirmed'].shift())
china_df['Daily Deaths'] = china_df['Deaths'].sub(china_df['Deaths'].shift())

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.bar(china_df.index, china_df['Daily Confirmed'], color='b',
       label='China Daily Confirmed')
ax.bar(china_df.index, china_df['Daily Deaths'], color='r',
       label='China Daily Deaths')
ax.set_xlabel('Date')
ax.set_ylabel('# of Cases')
ax.set_title('China Covid-19 Daily Cases')
plt.legend(loc='upper right')
plt.show()
"""

""" US Daily Cases and Deaths"""
worldwide_df['Daily Confirmed'] = worldwide_df['Confirmed'].sub(worldwide_df['Confirmed'].shift())
worldwide_df['Daily Deaths'] = worldwide_df['Deaths'].sub(worldwide_df['Deaths'].shift())

"""overlay
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

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121)
ax1.bar(worldwide_df.index, worldwide_df['Daily Confirmed'],
        color='gray')
ax1.set_title('Daily New Cases', fontsize=16)
ax1.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
ax2 = fig.add_subplot(122)
ax2.bar(worldwide_df.index, worldwide_df['Daily Deaths'],
        color='gray')
ax2.set_title('Daily Deaths', fontsize=16)
ax2.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
plt.xlabel('Date')
plt.ylabel('# of Cases')
plt.suptitle('Worldwide Covid-19 Daily Cases', fontsize=25)
plt.show()
"""

""" 7-day moving average
worldwide_df_avg7d = worldwide_df.rolling(7).mean()

fig = plt.figure(figsize=(12, 6))
ax = fig.add_axes([0, 0, 1, 1])
ax.grid(False)
ax1 = fig.add_subplot(121)
ax1.bar(worldwide_df_avg7d.index, worldwide_df_avg7d['Daily Confirmed'],
        color='gray')
ax1.set_title('Daily New Cases', fontsize=16)
ax1.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
ax1.set_xlabel('Date')
ax1.set_ylabel('# of Cases')
ax2 = fig.add_subplot(122)
ax2.bar(worldwide_df_avg7d.index, worldwide_df_avg7d['Daily Deaths'],
        color='gray')
ax2.set_title('Daily Deaths', fontsize=16)
ax2.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
ax2.set_xlabel('Date')
ax2.set_ylabel('# of Cases')
plt.suptitle('Worldwide Covid-19 Daily Cases', fontsize=30)
ax.text(x=0.5, y=0.02, s='7-day moving average', fontsize=22, ha='center')
plt.tight_layout()
plt.show()
"""

""" Pie Chart Top 10 Countries"""
yesterday = date.today() - timedelta(days=2)
today_df = df[df['Date'] == pd.Timestamp(yesterday)]
top_10 = today_df.sort_values(['Confirmed'], ascending=False)[:10]
top_10.loc['rest-of-world'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_10.loc['rest-of-world', 'Country'] = 'Rest of World'

"""
fig = plt.figure(figsize=(12, 10))
ax0 = fig.add_axes([0, 0, 1, 1])
ax0.grid(False)
ax = fig.add_subplot(111)


def func(pct, data):
    absolute = int(pct/100.*np.sum(data))
    return '{:.1f}%\n({:d})'.format(pct, absolute)


#explode = np.arange(0, 0.5, 0.05).tolist()
explode = np.arange(0.05, 0.3, 0.05).tolist()
explode = [0.02] + explode + explode[:-1:][::-1] +[0]
#explode[0] = 0.1

num_colors = len(top_10)
# https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
theme = plt.get_cmap('viridis')
ax.set_prop_cycle('color', [theme(1.*i/num_colors) for i in range(num_colors)])
_, texts, autotexts = ax.pie(top_10['Confirmed'], labels=top_10['Country'],
       autopct='%1.1f%%', startangle=0,
       pctdistance=0.9, labeldistance=1.1,
       shadow=True, explode=explode,
       #colors=colors
       # percentage + absolute value
       # autopct=lambda pct: func(pct, top_10['Confirmed']),
       # textprops={'color': 'w'}
        )
# fontsize, weight and color of 'labels')
plt.setp(texts, size=12, color='b')
#for text in texts:
#    text.set_fontsize(20)
#    text.set_color('b')
# fontsize, weight and color of 'percentage')
plt.setp(autotexts, size=10, weight='bold', color='w')
#plt.rcParams['font.size']=20
#for autotext in autotexts:
#    autotext.set_color('white')
plt.title('Hardest Hit Countries Worldwide',
         fontsize=30, fontweight='bold')
ax0.text(0.5, 0.85, 'Data updated on ' + yesterday.strftime('%Y-%m-%d'),
         ha='center', fontsize=20)
plt.legend(bbox_to_anchor=(1.25, 0.5), loc='right')
plt.show()
"""

fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(aspect='equal'))
num_colors = len(top_10)
# https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
theme = plt.get_cmap('plasma')
theme_color = [theme(1.*i/num_colors) for i in range(num_colors)]
ax.set_prop_cycle('color', theme_color)
wedges, texts, autotexts = ax.pie(top_10['Confirmed'],
                                  wedgeprops=dict(width=0.6),
                                  startangle=-45,
                                  autopct='%1.1f%%',
                                  pctdistance=0.75)
plt.setp(autotexts, size=10, weight='bold', color='w')
# 'square','circle','darrow','larrow','rarrow','round4'  face_color edge_color line_width
bbox_props = dict(boxstyle='round, pad=0.5', fc='gray', ec='r', lw=1.25)
kw = dict(arrowprops=dict(arrowstyle='<-', color='r', linewidth=1.25),
          bbox=bbox_props, zorder=0, va='center', ha='center',
          size=10, color='w')

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontal_alignment = {-1: 'right', 1: 'left'}[int(np.sign(x))]
    connection_style = 'angle, angleA=0, angleB=90{}'.format(ang)
    kw['bbox'].update({'fc': theme_color[i]})
    kw['arrowprops'].update({'connectionstyle': connection_style})
    ax.annotate(top_10.iloc[i, 1], xy=(x, y), xycoords='data',
                xytext=(1.35*np.sign(x), 1.25*y),
                textcoords='data',
                horizontalalignment=horizontal_alignment, **kw)
plt.title('Hardest Hit Countries Worldwide',
         fontsize=30, fontweight='bold')
ax.text(0, 0, 'Data updated\n' + yesterday.strftime('%Y-%m-%d'),
         ha='center', va='center', fontsize=15)
plt.show()

