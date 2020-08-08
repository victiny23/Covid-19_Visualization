import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
plt.style.use('fivethirtyeight')

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

yesterday = date.today() - timedelta(days=1)
today_df = df[df['Date'] == pd.Timestamp(yesterday)]
top_10 = today_df.sort_values(['Confirmed'], ascending=False)[:10]
top_10.loc['rest-of-world'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_10.loc['rest-of-world', 'Country'] = 'Rest of World'


def func(pct, data):
    absolute = int(pct/100.*np.sum(data))
    return '{:.1f}%\n({:d})'.format(pct, absolute)


fig = plt.figure(figsize=(12, 12))
ax0 = fig.add_axes([0, 0, 1, 1])
ax0.grid(False)
ax = fig.add_subplot(111)

# sticking out slices
explode = np.arange(0.05, 0.3, 0.05).tolist()
explode = [0.02] + explode + explode[:-1:][::-1] +[0]

# set a list of colors to use
num_colors = len(top_10)
# https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
theme = plt.get_cmap('viridis')
theme_colors = [theme(1.*i/num_colors) for i in range(num_colors)]
ax.set_prop_cycle('color', theme_colors)
_, texts, autotexts = ax.pie(top_10['Confirmed'], labels=top_10['Country'],
       autopct='%1.1f%%', startangle=0,
       pctdistance=0.9, labeldistance=1.1,
       shadow=True, explode=explode,
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
# plt.rcParams['font.size']=20
# for autotext in autotexts:
#    autotext.set_color('white')
plt.title('Hardest Hit Countries Worldwide',
          fontsize=30, fontweight='bold')
ax0.text(0.5, 0.85, 'Data updated on ' + yesterday.strftime('%Y-%m-%d'),
         ha='center', fontsize=20)
lg = plt.legend(title='Country', title_fontsize=18,
                fontsize=12,
                bbox_to_anchor=(1.25, 0.5), loc='right')
plt.show()