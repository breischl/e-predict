# e-predict
The goal of this project is to develop an ML model capable of forecasting daily electric demand in the 
Public Service Company of Colorado (PSCO, basically XCel Energy's footprint in Colorado) territory, based on the forecast daily temperatures. 

## Status
Very much in development. As seems to be standard for ML projects, acquiring training data is taking quite a while. 

Thus far I have:
 - identified data sources (see below)
 - written a client library to retrieve weather forecasts from NOAA/weather.gov, in the `noaa_client` package.
 - written download and parsing code to retrieve historical weather data from GHCN-D in the `ghcnd` package.

My next step is writing a client for EIA OpenData to get daily electric usage data.

## Data Sources
I have identified three data sources that I believe will get me sufficient information.

1. [EIA OpenData](https://www.eia.gov/opendata/) has electric demand data back to 2015, and provides daily updates
2. [NOAA Weather](https://www.weather.gov/documentation/services-web-api) provides forecast data (including temp) but very limited historical data (only 7 days, and only on some endpoints)
3. [NOAA's GHCN-d dataset](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) provides historical weather data. In particular, it can be [downloaded from here](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/)


