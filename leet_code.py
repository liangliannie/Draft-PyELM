from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.
m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
m.drawcoastlines()
m.fillcontinents(color='beige',lake_color='lightblue')
# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,30.),color='gray',dashes=[1,3],labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,181.,60.),color='gray',dashes=[1,3],labels=[0,0,0,1])
m.drawmapboundary(fill_color='lightblue')
plt.title('Site Analysis')
# plot blue dot on Boulder, colorado and label it as such.
lon, lat = -104.237, 40.125 # Location of Boulder
xpt,ypt = m(lon,lat)
lonpt, latpt = m(xpt,ypt,inverse=True)
m.plot(xpt,ypt,'bo',label='Boulder')  # plot a blue dot there
# put some text next to the dot, offset a little bit
# (the offset is in map projection coordinates)
# plt.text(xpt,ypt,'Boulder (%5.1fW,%3.1fN)' % (lonpt,latpt))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()