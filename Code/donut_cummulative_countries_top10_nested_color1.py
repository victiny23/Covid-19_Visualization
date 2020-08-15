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
top_10 = today_df.sort_values(['Confirmed'], ascending=False)[:10]
top_10.loc['rest-of-world'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_10.loc['rest-of-world', 'Country'] = 'Rest of World'

# width of the donut
size = 0.3
# values for chart
vals1 = []
for i in range(len(top_10)):
    # [['Recovered'], ['Active'], ['Deaths']]
    val = [top_10.iloc[i][5], top_10.iloc[i][3] + top_10.iloc[i][4]]
    vals1.append(val)
vals1 = np.array(vals1)

cmap = plt.get_cmap('plasma')
num_colors = len(top_10) * 3
theme_colors = [cmap(1.*i/num_colors) for i in range(num_colors)]
outer_colors = theme_colors[0:num_colors:3]
inner_colors = [c for c in theme_colors if c not in outer_colors]

fig, ax = plt.subplots(figsize=(12, 12))

_, texts, autotexts = ax.pie(vals1.sum(axis=1), labels=top_10['Country'],
       autopct='%1.1f%%', pctdistance=0.85,
       radius=1, colors=outer_colors,
       wedgeprops=dict(width=size, edgecolor='w'))
for i in range(len(top_10)):
    plt.setp(texts[i], size=12, weight='bold', color=outer_colors[i])
plt.setp(autotexts, size=10, weight='bold', color='w')
sub_label = [''] *(len(top_10) -1)*2 + ['Active', 'Recovered\nor\nDeaths']
_, sub_texts = ax.pie(vals1.flatten(),
                              labels=sub_label, labeldistance=0.8,
                              rotatelabels=True,
                              radius=1-size, colors=inner_colors,
                              wedgeprops=dict(width=size, edgecolor='w'))
plt.setp(sub_texts, rotation_mode='anchor',
         ha='center', va='center',
         size=12, weight='bold', color='k')
for tx in sub_texts:
    rot = tx.get_rotation()
    if rot < 180:
        tx.set_rotation(rot - 90)
    if rot > 180:
        tx.set_rotation(rot-270)
    print(rot)
plt.title('Hardest Hit Countries Worldwide',
         fontsize=30, fontweight='bold')
ax.text(0, 0, 'Data updated\n' + yesterday.strftime('%Y-%m-%d'),
         ha='center', va='center', fontsize=15)
plt.show()


