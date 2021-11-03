# This script processes the 2020 SLO County presidential election precincts file, and
# generates:
# adjlist: list of length precincts of all adjacency precincts
# centroids: list of the geometric means of each precincts
# distancemat: square distances matrix between centroids of precinct
# area: numeric vector of area of each precinct
# centers: 2d list of coordinates (x,y) of precinct centroids
# colors: 5-hexcode vector used to color maps

library(tidyverse)
library(sf)
library(redist)
library(sp)
library(spData)
library(spdep)

# unzip zip file that has the shapefiles in into temp directory
unzip("shp/slo_2020_precincts_districts_votes.zip", exdir="shp/slo_2020_precincts_districts_votes")
# read in the shapefile
df <- st_read("shp/slo_2020_precincts_districts_votes/slo_2020_precincts_districts_votes.shp")
# delete the extracted files. 
unlink("shp/slo_2020_precincts_districts_votes", recursive=TRUE)

adjlist <- redist.adjacency(df)
centroids <- sf::st_centroid(df)
distancemat <- sf::st_distance(centroids, centroids)
area <- sf::st_area(df)
centers <- sf::st_coordinates(centroids)
# add row_n as unique precinct identifier to join on for plots
df$row_n <- seq.int(nrow(df))
# CRSG requires integer population
df$pop_int <- round(df$pop)
colors <- c("#E6194B", "#F58231", "#FFE119", "#3CB44B", "#4363DB")

save.image(file = "data/data.RData")
