The best public electric production/consumption data I've found thus far is from the EIA, non-shockingly. 

# Dashboard 
There's a [nice graphical dashboard](https://www.eia.gov/electricity/gridmonitor/dashboard/electric_overview/US48/US48) 
which can be further broken down by Balancing Authority and probably other things. Some data are provided down to hourly granularity. 
For my initial purposes here, the [dashboard focused on PSCO](https://www.eia.gov/electricity/gridmonitor/dashboard/electric_overview/balancing_authority/PSCO) is the most relevant. 

Note also that the "Download Data" button gives an plethora of really useful options. The little "i-for-information" buttons are 
surprisingly helpful as well. Overall this is a really fantastic dashboard that's a great place to start. 

# EIA OpenData API
EIA's [OpenData site](https://www.eia.gov/opendata/) is similarly helpful, and in particular the [RTO generation API](https://www.eia.gov/opendata/browser/electricity/rto/daily-region-data). For our purposes, select the Route for "Daily Demand, Demand Forecast, (etc)" and then "Filter by Facet" feature to Respondent=PSCO. 

The API URL we want to use is like: `https://api.eia.gov/v2/electricity/rto/region-data/data?data%5B%5D=value&facets%5Brespondent%5D%5B%5D=PSCO&frequency=hourly&start=2021-01-01&end=2021-01-02&api_key=API-KEY-GOES-HERE`

### Aside: Data limitations
I would've liked to get daily breakdowns by fuel/generation type, so that would could attempt to forecast solar & wind generation specifically.
Unfortunately EIA OpenData fuel type breakdowns are only provided at monthly granularity, so that won't be possible without a different data source. 

# OpenData Clients
There are a number of EIA OpenData clients for Python ([EIA-python](https://github.com/mra1385/EIA-python), [PyEIA](https://pypi.org/project/pyeia/), [EnerPy](https://pypi.org/project/EnerPy/)) but all seem to be for different sets of endpoints than what we need.

Given that what I need right now is literally one GET request, it doesn't seem worth building or importing a whole client library. 