import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
# Worldwide Cases
worldwide_df = df.groupby(['Date']).sum()
# Worldwide Daily Cases and Deaths
worldwide_df['Daily Confirmed'] = worldwide_df['Confirmed'].sub(worldwide_df['Confirmed'].shift())
worldwide_df['Daily Deaths'] = worldwide_df['Deaths'].sub(worldwide_df['Deaths'].shift())
time_stamps = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121)
ax1.bar(worldwide_df.index, worldwide_df['Daily Confirmed'],
        color='gray')
ax1.set_title('Daily New Cases', fontsize=16)
ax1.set_xticklabels(time_stamps,
                    fontsize=12, rotation=30)
ax1.set_xlabel('Date', fontsize=15)
ax1.set_ylabel('# of Cases', fontsize=15)
ax2 = fig.add_subplot(122)
ax2.bar(worldwide_df.index, worldwide_df['Daily Deaths'],
        color='gray')
ax2.set_title('Daily Deaths', fontsize=16)
ax2.set_xticklabels(time_stamps,
                    fontsize=12, rotation=30)
ax2.set_xlabel('Date', fontsize=15)
ax2.set_ylabel('# of Cases', fontsize=15)
plt.suptitle('Worldwide Covid-19 Daily Cases', fontsize=25)
plt.show()