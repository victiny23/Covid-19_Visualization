import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
# active cases
df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']

yesterday = date.today() - timedelta(days=2)
today_df = df[df['Date'] == pd.Timestamp(yesterday)]
top_4 = today_df.sort_values(['Confirmed'], ascending=False)[:4]
top_4.loc['rest-of-world'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_4.loc['rest-of-world', 'Country'] = 'Rest of World'

# width of the donut
size = 0.3
# values for chart
vals1 = []
for i in range(len(top_4)):
    # [['Recovered'], ['Active'], ['Deaths']]
    val = [top_4.iloc[i][3], top_4.iloc[i][5], top_4.iloc[i][4]]
    vals1.append(val)
# convert list to np.array
vals1 = np.array(vals1)

# set up colors
cmap = plt.get_cmap('tab20c')
# [0, 4, 8, 12, 16]
outer_colors = cmap(np.arange(5)*4)
inner_colors = cmap(np.array([1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15,
                              17, 18, 19]))

fig, ax = plt.subplots(figsize=(12, 12))
_, texts, autotexts = ax.pie(vals1.sum(axis=1), labels=top_4['Country'],
                             autopct='%1.1f%%', pctdistance=0.85,
                             radius=1, colors=outer_colors,
                             wedgeprops=dict(width=size, edgecolor='w'))
# colors of outer labels
for i in range(len(top_4)):
    plt.setp(texts[i], size=12, weight='bold', color=outer_colors[i])
plt.setp(autotexts, size=10, weight='bold', color='w')
# show labels only for the first country
sub_label = ['Recovered', 'Active', 'Deaths'] + [''] *12
_, sub_texts = ax.pie(vals1.flatten(),
                      labels=sub_label, labeldistance=0.8,
                      rotatelabels=True,
                      radius=1-size, colors=inner_colors,
                      wedgeprops=dict(width=size, edgecolor='w'))
plt.setp(sub_texts, rotation_mode='anchor',
         ha='center', va='center', size=8, color='k')
# rotate the sub_labels
for tx in sub_texts:
    rot = tx.get_rotation()
    if rot > 180:
        tx.set_rotation(rot-180)
plt.title('Hardest Hit Countries Worldwide',
         fontsize=30, fontweight='bold')
ax.text(0, 0, 'Data updated\n' + yesterday.strftime('%Y-%m-%d'),
         ha='center', va='center', fontsize=15)
plt.show()


