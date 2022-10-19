# e-predict
The goal of this project is to develop an ML model capable of forecasting daily electric demand in the 
Public Service Company of Colorado (PSCO, basically XCel Energy in Colorad) territory, based on the forecast daily temperatures. 

## Status
Very much in development. As seems to be standard for ML projects, acquiring training data is taking quite a while. 

I have identified three data sources that I believe will get me sufficient information.

1. [EIA OpenData](https://www.eia.gov/opendata/) has electric demand data back to 2015, and provides daily updates
2. [NOAA Weather](https://www.weather.gov/documentation/services-web-api) provides forecast data (including temp) but very limited historical data (only 7 days, and only on some endpoints)
3. [NOAA's Climate Data Online (CDO)](https://www.ncdc.noaa.gov/cdo-web/webservices/v2) provides historical weather data

I have coded up a client for the NOAA Weather API (in the `noaa_client` package). My next step is acquiring historical data from CDO.

