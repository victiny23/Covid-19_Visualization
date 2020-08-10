import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.patches as patches
from datetime import date, timedelta
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])

yesterday = date.today() - timedelta(days=1)
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


# define a function to insert image to pie chart
def img_to_pie(fn, wedge, xy, zoom=1, ax=None):
    if ax == None:
        ax = plt.gca()
    # im = plt.imread(fn, format='png'), if no conversion to PIL image
    im = fn
    path = wedge.get_path()
    patch = patches.PathPatch(path, facecolor='none')
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


fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(aspect='equal'))
num_colors = len(top_10)
# https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
theme = plt.get_cmap('plasma')
theme_color = [theme(1.*i/num_colors) for i in range(num_colors)]
ax.set_prop_cycle('color', theme_color)

wedges, _ = plt.pie(top_10['Confirmed'],
                        # labels=labels,
                        startangle=-45,
                        # labeldistance=1.1,
                        wedgeprops={'linewidth': 1.75,
                                    'edgecolor': 'w',
                                    'width': 0.5,
                                    'fill': False})
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
    ax.annotate(labels[i], xy=(x, y), xycoords='data',
                xytext=(1.35*np.sign(x), 1.2*y),
                textcoords='data',
                horizontalalignment=horizontal_alignment, **kw)

positions = []
angles = []
for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    angles.append(ang)
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    position = (x*0.8, y*0.5)
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
""""""
plt.title('Hardest Hit Countries Worldwide',
         fontsize=28, fontweight='bold')
ax.text(1.3, -1.1, 'Data updated\n' + yesterday.strftime('%Y-%m-%d'),
         ha='center', va='center', fontsize=15, color='#484D8B')

# Add patch in the center of the donut
center_patch = plt.imread('C:\\Users\\Victiny\\Python_Project\\Covid-19_Visualization\\Flag\\virus.jpg',
                          format='jpg')
cp_im = Image.fromarray(255 - np.uint8(center_patch*255))
width, height = cp_im.size
diff = (width - height)/2
left, right = diff, width - diff
cp_im_crop = cp_im.crop((left, 0, right, height))
imc = ax.imshow(cp_im_crop, extent=(-0.55, 0.55, -0.55, 0.55))
patch = patches.Circle((0, 0), radius=0.55,
                       transform=ax.transData, color='gray', fill=False)

imc.set_clip_path(patch)
""""""
ax.axis('off')
plt.show()


