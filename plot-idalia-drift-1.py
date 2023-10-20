import pickle
import geopandas as gpd

with open('../wavespec/hurricane_idalia_drifter_data_v1.pickle', 'rb') as f1:
    spots = pickle.load(f1)

run -i "plot-drift-swh-1.py"

gd1 = gpd.read_file('idalia_best_track/AL102023_pts.shp')
lt1 = gd1.LAT
ln1 = gd1.LON
hurpth = np.array(list(zip(ln1,lt1)))

for btype in spots.keys():
    for buoy1 in spots[btype].keys():
        df1 = spots[btype][buoy1]
        dt1, df1a = drift_clean(df1, ("2023-08-29 23:31", "2023-08-30 12:30"))
        out1 = drift_swhplt(dt1, df1a.significant_height, df1a.latitude, df1a.longitude, btype=btype, name=buoy1,
                            extent=(-88, -82.2, 24.3, 30.3), hurrpath=hurpth)
        savestr = f'Idalia_{btype}-{buoy1}_swh'
        plt.savefig(f'idalia_drft/{savestr}.png',dpi=200)
        plt.close()

