import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

yesterday = date.today() - timedelta(days=1)
today_df = df[df['Date'] == pd.Timestamp(yesterday)]
top_10 = today_df.sort_values(['Confirmed'], ascending=False)[:10]
top_10.loc['rest-of-world'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_10.loc['rest-of-world', 'Country'] = 'Rest of World'

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
kw = dict(arrowprops=dict(arrowstyle='<|-', color='r', linewidth=1.25),
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

