import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
# active cases
df['Active'] = df['Confirmed'] - df['Recovered'] -df['Deaths']

yesterday = date.today() - timedelta(days=2)
today_df = df[df['Date'] == pd.Timestamp(yesterday)]
top_10 = today_df.sort_values(['Confirmed'], ascending=False)[:10]
top_10['Region'] = ['NA', 'SA', 'Asia', 'Euro', 'Africa', 'NA', 'SA', 'SA', 'SA', 'Euro']

# group by region
grouped_df = top_10.groupby(['Region'])
# create a new column for region sum
top_10['Region Sum'] = grouped_df[['Confirmed']].transform(sum)
# sort by region sum, descending
top_10 = top_10.sort_values(['Region Sum'], ascending=False)
top_10_agg = top_10.groupby(top_10['Region']).sum().sort_values(['Confirmed'], ascending=False)

top_10.loc['rest-of-world'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_10.loc['rest-of-world', 'Country'] = 'Rest of World'
top_10.loc['rest-of-world', 'Region'] = 'Rest of World'
top_10.loc['rest-of-world', 'Region Sum'] = top_10.loc['rest-of-world', 'Confirmed']

top_10_agg.loc['Rest of World'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_10_agg.loc['Rest of World', 'Region Sum'] = top_10.loc['rest-of-world', 'Confirmed']

# width of the donut
size = 0.3
# values for chart
outer_vals = top_10['Confirmed']
inner_vals = top_10_agg['Confirmed']

cmap = plt.get_cmap('plasma')
num_colors = len(top_10) + len(top_10_agg)
theme_colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

country_in_group = top_10.groupby('Region Sum').size().tolist()
last = country_in_group.pop()
country_in_group = country_in_group[::-1]

inner_colors = [theme_colors[0]]
color0 = 0
for size_group in country_in_group:
    inner_colors.append(theme_colors[color0 + size_group + 1])
    color0 = color0 + size_group + 1
outer_colors = [c for c in theme_colors if c not in inner_colors]

region_list = ['North\nAmerica', 'South\nAmerica', 'Asia', 'Europe', 'Africa', 'Rest of\nWorld']

fig, ax = plt.subplots(figsize=(12, 12))
# outer ring
_, texts, autotexts = ax.pie(outer_vals, labels=top_10['Country'],
                             autopct='%1.1f%%', pctdistance=0.9,
                             radius=0.8+size, colors=outer_colors,
                             wedgeprops=dict(width=size, edgecolor='w'))
for i in range(len(top_10)):
    plt.setp(texts[i], size=12, weight='bold', color=outer_colors[i])
plt.setp(autotexts, size=10, weight='bold', color='w')
# inner ring
_, texts = ax.pie(inner_vals, labels=region_list,
                  labeldistance=0.8,
                  # rotatelabels=True,
                  radius=0.8, colors=inner_colors,
                  wedgeprops=dict(width=size, edgecolor='w'))
plt.setp(texts, size=10, weight='bold', color='w', rotation_mode='anchor',
         ha='center', va='center')
plt.title('Hardest Hit Countries Worldwide', y=1,
         fontsize=30, fontweight='bold')
ax.text(0, 0, 'Data updated\n' + yesterday.strftime('%Y-%m-%d'),
         ha='center', va='center', fontsize=15)
plt.show()