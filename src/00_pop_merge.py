import geopandas
import pandas as pd

# read in block groups shapefile
bg = geopandas.read_file("zip://data/ca_2020_blck_grp_shp.zip")
# keep only the useful cols
bg = bg[["GEOID", "GISJOIN", "geometry"]].copy()
# read in population data csv
data = pd.read_csv("data/ca_2020_blck_grp_pop.csv")

# # keep only the relevant columns for total population by race.
# U7B001:      Total
# U7B003:      Population of one race: White alone
# U7B004:      Population of one race: Black or African American alone
# U7B005:      Population of one race: American Indian and Alaska Native alone
# U7B006:      Population of one race: Asian alone
# U7B007:      Population of one race: Native Hawaiian and Other Pacific Islander alone
# U7B008:      Population of one race: Some Other Race alone
# U7B009:      Population of two or more races

data = data[["GISJOIN", "COUNTY", "U7B001", "U7B003", "U7B004", "U7B005", "U7B006", 
            "U7B007", "U7B008", "U7B009"]].copy()
# rename these cols to something more intelligible
data.columns = ["GISJOIN", "COUNTY", "pop", "white_pop", "black_pop", "aian_pop", "asian_pop", 
                "nhopi_pop", "sor_pop", "2more_pop"]
# merge the population data into the bg shapefile
bg = bg.merge(data, on='GISJOIN')

# keep only the SLO county block groups. Go from 307068 to 2160 block groups
bg = bg[bg["COUNTY"] == "San Luis Obispo County"].copy()

# write bg to file
out_file = "data/slo_2020_blck_grp_shp_pop.shp"
bg.to_file(out_file)
# best to zip manually now (too lazy to use shutil)