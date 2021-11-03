## I need to add in which supervisor district each precinct is in using maup.

import maup
import geopandas
import warnings

# enable progress bar for all maup operations
maup.progress.enabled = True
# turn off annoying geopandas warnings
warnings.filterwarnings('ignore', 'GeoSeries.isna', UserWarning)

precincts = geopandas.read_file("zip://shp/slo_2020_president_precincts_race.zip")
sd = geopandas.read_file("zip://shp/slo_supervisor_districts.zip")

# reproject files to CA Albers via CRs
precincts = precincts.to_crs(epsg=3310)
sd = sd.to_crs(epsg=3310)
# remove any bowties (little imperfections in the polygons)
precincts.geometry = precincts.buffer(0)
sd.geometry = sd.buffer(0)
# reset index
precincts = precincts.reset_index(drop = True)
sd = sd.reset_index(drop = True)

# assign a supervisor district to each precinct based on overlapping geometry. 
assignment = maup.assign(precincts, sd)
precincts["SUPDIST"] = assignment

out_file = "shp/slo_2020_precincts_districts_votes.shp"
precincts.to_file(out_file)
# manually zip up files after 