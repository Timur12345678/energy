import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

fname = 'energy.csv'

# Read in the data, but I skipped setting the index and made sure no data
# is lost to a nonexistent header
df = pd.read_csv(fname, parse_dates=[0], header=None, names=['datetime', 'watt'])

# We want to separate the date from the time, so create two new columns
df['date'] = [x.date() for x in df['datetime']]
df['time'] = [x.time() for x in df['datetime']]

# Now we want to reshape the data so we have dates and times making the result 2D
pv = df.pivot(index='time', columns='date', values='watt')

# Not every date has every time, so fill in the subsequent NaNs or there will be holes
# in the surface
pv = pv.fillna(0.0)

# Now, we need to construct some arrays that matplotlib will like for X and Y values
xx, yy = np.mgrid[0:len(pv),0:len(pv.columns)]

# We can now plot the values directly in matplotlib using mplot3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(xx, yy, pv.values, cmap='jet', rstride=1, cstride=1)
ax.grid(False)

# Now we have to adjust the ticks and ticklabels - so turn the values into strings
dates = [x.strftime('%Y-%m-%d') for x in pv.columns]
times = [str(x) for x in pv.index]

# Setting a tick every fifth element seemed about right
ax.set_xticks(xx[::5,0])
ax.set_xticklabels(times[::5])
ax.set_yticks(yy[0,::5])
ax.set_yticklabels(dates[::5])

plt.show()