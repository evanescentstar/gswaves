import pickle
import geopandas as gpd
import cartopy.crs as crs
import cartopy.feature as cf
import matplotlib.pyplot as plt

with open('../wavespec/hurricane_idalia_drifter_data_v1.pickle', 'rb') as f1:
    spots = pickle.load(f1)

gd1 = gpd.read_file('idalia_best_track/AL102023_pts.shp')
lt1 = gd1.LAT
ln1 = gd1.LON
hurpth = np.array(list(zip(ln1,lt1)))

cpc = crs.PlateCarree()

fig1 = plt.figure()
ax1 = fig1.add_axes((0.12, 0.125, 0.8, 0.8),projection=cpc)
ax1.set_extent([-88.5, -81, 23.3, 30.3])
ax1.add_feature(cf.STATES, edgecolor='lightblue', linewidth=1, zorder=-1)

ax1.plot(hurpth[:,0],hurpth[:,1],'*-', markersize=3, linewidth=1, c='gray', zorder=5)

for btype in spots.keys():
    for buoy1 in spots[btype].keys():
        df1 = spots[btype][buoy1]
        dt1, df1a = drift_clean(df1, ("2023-08-29 23:31", "2023-08-30 12:30"))
        ax1.scatter(df1a.longitude, df1a.latitude, s=5, marker='.', c=dt1, cmap=cm.turbo, zorder=6)
        if 'swift' in btype:
            bt2 = 'swift'
        elif 'spot' in btype:
            bt2 = 'spt'
            # This line uses the last four digits of the buoy number to annotate it on the map
            buoy2 = buoy1[-4:]
        elif 'dwsd' in btype:
            bt2 = btype
            # This line uses the last four digits of the buoy number to annotate it on the map
            buoy2 = buoy1[-4:]
        ax1.annotate(f'{bt2}_{buoy2}', xy=(df1a.longitude[0], df1a.latitude[0]), size=7)

xtl = ax1.get_xticklabels()
ax1.set_xticklabels(xtl, size=7)
ytl = ax1.get_yticklabels()
ax1.set_yticklabels(ytl, size=9)
