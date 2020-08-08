import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import approaches_download_img as adi

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

yesterday = date.today() - timedelta(days=2)
today_df = df[df['Date'] == pd.Timestamp(yesterday)]
top_10 = today_df.sort_values(['Confirmed'], ascending=False)[:10]
top_10.loc['rest-of-world'] = today_df.sort_values(['Confirmed'], ascending=False)[10:].sum()
top_10.loc['rest-of-world', 'Country'] = 'Rest of World'
countries = top_10['Country'].to_list()
# adapt to the url
countries[0] = 'united-states-of-america'
countries[4] = 'south-africa'

# file_names used to save downloaded image
filenames = []
# source of the image
img_urls = []
for i in range(len(top_10)-1):
    filename = 'C:\\Users\\Victiny\\Python_Project\\Covid-19_Visualization\\Flag\\' + countries[i].lower() + '.png'
    img_url = 'https://cdn.countryflags.com/thumbs/' + countries[i].lower() + '/flag-800.png'
    filenames.append(filename)
    img_urls.append(img_url)
# manually added flag of the earth
filenames.append('C:\\Users\\Victiny\\Python_Project\\Covid-19_Visualization\\Flag\\world.png')

"""
# download flags of top 10 countries
for i in range(len(top_10)):
    adi.app_requests(img_urls[i], filenames[i])

# show flags of top 10 countries
fig = plt.figure(figsize=(12, 8))
for i, filename in enumerate(filenames):
    ax = fig.add_subplot(3, 4, i + 1)
    img = plt.imread(filename)
    plt.imshow(img)
    ax.set_title(top_10['Country'].to_list()[i], fontsize=15)
plt.show()
"""


# define a function to insert image to pie chart
def img_to_pie(fn, wedge, xy, zoom=1, ax=None):
    if ax == None:
        ax = plt.gca()
    # im = plt.imread(fn, format='png'), if no conversion to PIL image
    im = fn
    path = wedge.get_path()
    patch = PathPatch(path, facecolor='none')
    ax.add_patch(patch)
    imagebox = OffsetImage(im, zoom=zoom, clip_path=patch, zorder=-10)
    ab = AnnotationBbox(imagebox, xy, xycoords='data', pad=0, frameon=False)
    ax.add_artist(ab)


# calculate the percentage
pct = top_10['Confirmed'].to_list()
world_sum = int(top_10['Confirmed'].sum())
pct = [p / world_sum for p in pct]
# labels: country + percentage
labels = []
for i in range(len(top_10)):
    label_country = top_10['Country'].to_list()[i]
    label_pct = '{:.1%}'.format(pct[i])
    label = label_country + ": " + label_pct
    labels.append(label)
# pie chart
fig = plt.figure(figsize=(12, 12))
wedges, texts = plt.pie(top_10['Confirmed'],
                        labels=labels,
                        startangle=0,
                        labeldistance=1.1,
                        wedgeprops={'linewidth': 1.75,
                                    'edgecolor': 'k',
                                    'fill': False})  # color in slice if True
# set the center of the figure as (0, 0)
plt.gca().axis('equal')
# position to insert the image
positions = []
angles = []
for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    angles.append(ang)
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    position = (x*0.8, y*0.58)
    positions.append(position)
# resize the image
zooms = [1.0] * (len(top_10)-1)
zooms.append(800 / 1803)
zooms = [zoom * 0.6 for zoom in zooms]

# call a function to insert image to pie chart
for i in range(len(top_10)):
    fn = filenames[i]
    # read the png to np.array
    img = plt.imread(fn)
    # convert np.array to PIL image
    im = Image.fromarray(np.uint8(img*255))
    img_to_pie(im.rotate(-90+angles[i]), wedges[i], xy=positions[i], zoom=zooms[i])
    wedges[i].set_zorder(10)

plt.setp(texts, size=15, color='b', weight='bold')
plt.title('Hardest Hit Countries Worldwide', y=1.05,
          fontsize=25, fontweight='bold')
plt.suptitle('Data updated on ' + yesterday.strftime('%Y-%m-%d'),
             y=0.9, color='#484D8B',
             ha='center', fontsize=20)
plt.show()



