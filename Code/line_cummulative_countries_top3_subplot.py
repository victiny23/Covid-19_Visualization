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

# Top 10 countries with the most cases
total_country_df = df.groupby(['Country']).sum()
total_country_df = total_country_df.\
        sort_values(['Confirmed'], ascending=[0])
total_country_top10 = list(total_country_df.index[0:10])

# plot the cases in countries top 3
fig = plt.figure(figsize=(15, 5))
for i in range(3):
    ax = fig.add_subplot(1, 3, i+1)
    country_df = df[df['Country'] == total_country_top10[i]].groupby(['Date']).sum()
    ax.plot(country_df.iloc[:, :3], #label= column_list[i],
            linestyle='solid', alpha=0.6)
    if i < 1:
        ax.legend(list(worldwide_df.columns),
                  loc='upper left')
    ax.set_xlabel('Date')
    ax.set_ylabel('# of Cases')
    ax.set_xticklabels(time_stamps,
                       fontsize=12, rotation=30)
    ax.set_ylim(-.1e6, 5e6)
    ax.title.set_text(str(total_country_top10[i]))
plt.suptitle('Countries with the most cases', fontsize=25)
plt.tight_layout()
plt.show()