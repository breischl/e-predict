There are a number of ways to find historical weather data. 

The best for my purposes seems to be the [Global Historical Climatology Network daily (GHCNd)](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) from NOAA. There are a number of data products from there. 

### /Pub/Data Downloads
[Daily file downloads](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/) are available from NCDC. The data files use
a fixed-width encoding that should be relatively efficient, but is a bit of a pain to parse. This was implemented in the `/ghcnd` subdirectory.

### NCEI Daily Downloads
[NCEI's daily index](https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/) appears to provide CSV-formatted
downloads for each weather station. Given that I need a small number of stations, and that CSV is readily parseable, this
would seem to be ideal. Sadly, the CSVs appear to be mangled by having some of the commas inside quotes, so they get treated as values. 
Un-mangling the CSV would probably be possible, but seems potentially buggy and obnoxious. 

### NCDC CDO
Climate Data Online provides an [HTTP API for accessing the data](https://www.ncdc.noaa.gov/cdo-web/webservices/v2). This would probably be ideal for small-scale updates (eg, getting the latest few days worth of data) but there are better options for bulk historical data.

# Finding Station IDs
There is [an online map of GHCN stations](https://ncics.org/portfolio/monitor/ghcn-d-station-data/) that is convenient
for small-scale, manual mapping. Otherwise each of the previously-mentioned data sources has various ways of finding station identifiers. 
