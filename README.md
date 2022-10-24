# e-predict
The goal of this project is to develop an ML model capable of forecasting daily electric demand in the 
Public Service Company of Colorado (PSCO, basically XCel Energy's footprint in Colorado) territory, based on the forecast daily temperatures. 

## Status
Very much in development. I'm currently working on analyzing the historical data. 

Thus far I have:
 - identified data sources (see below)
 - written a client library to retrieve weather forecasts from NOAA/weather.gov, in the `noaa_client` package.
 - written download and parsing code to retrieve historical weather data from GHCN-D in the `ghcnd` package.
 - written download and parsing code for the EIA OpenData historical electric demand data in the `eia` package.
 - Begun work on a Jupyter notebook (in `explore_temp_data.ipynb`) to analyze that data


## Data Sources
I have identified three data sources that I believe will get me sufficient information.

1. [EIA OpenData](https://www.eia.gov/opendata/) has electric demand data back to 2015, and provides daily updates
2. [NOAA Weather](https://www.weather.gov/documentation/services-web-api) provides forecast data (including temp) but very limited historical data (only 7 days, and only on some endpoints)
3. [NOAA's GHCN-d dataset](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) provides historical weather data. In particular, it can be [downloaded from here](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/)


