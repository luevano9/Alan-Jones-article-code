from tkinter import Y
import pandas as pd
import streamlit as st
import requests
import io
import plotly.express as px


#################### Data
stations = [
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/aberporthdata.txt', 'name':'Aberporth'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/armaghdata.txt', 'name':'Armagh'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/ballypatrickdata.txt', 'name':'Ballypatrick Forest'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/bradforddata.txt', 'name':'Bradford'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/braemardata.txt', 'name':'Braemar'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/cambornedata.txt', 'name':'Camborne'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/cambridgedata.txt', 'name':'Cambridge NIAB'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/cardiffdata.txt', 'name':'Cardiff Bute Park'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/chivenordata.txt', 'name':'Chivenor'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/cwmystwythdata.txt', 'name':'Cwmystwyth'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/dunstaffnagedata.txt', 'name':'Dunstaffnage'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/durhamdata.txt', 'name':'Durham'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/eastbournedata.txt', 'name':'Eastbourne'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/eskdalemuirdata.txt', 'name':'Eskdalemuir'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/heathrowdata.txt', 'name':'Heathrow'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/hurndata.txt', 'name':'Hurn'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/lerwickdata.txt', 'name':'Lerwick'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/leucharsdata.txt', 'name':'Leuchars'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/lowestoftdata.txt', 'name':'Lowestoft'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/manstondata.txt', 'name':'Manston'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/nairndata.txt', 'name':'Nairn'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/newtonriggdata.txt', 'name':'Newton Rigg'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/oxforddata.txt', 'name':'Oxford'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/paisleydata.txt', 'name':'Paisley'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/ringwaydata.txt', 'name':'Ringway'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/rossonwyedata.txt', 'name':'Ross-on-Wye'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/shawburydata.txt', 'name':'Shawbury'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/sheffielddata.txt', 'name':'Sheffield'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/southamptondata.txt', 'name':'Southampton'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/stornowaydata.txt', 'name':'Stornoway Airport'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/suttonboningtondata.txt', 'name':'Sutton Bonington'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/tireedata.txt', 'name':'Tiree'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/valleydata.txt', 'name':'Valley'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/waddingtondata.txt', 'name':'Waddington'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/whitbydata.txt', 'name':'Whitby'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/wickairportdata.txt', 'name':'Wick Airport'},
{'url':'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/yeoviltondata.txt', 'name':'Yeovilton'}
]

station_names = [stations[n]['name'] for n in range(len(stations))] 

# create dataframe from text file and add a date column
def makedf(i):

    url = stations[i]['url']
    file = io.StringIO(requests.get(url).text)

    col_names = ('Year','Month','Tmax','Tmin','AF','Rain','Sun','status')

    weather = pd.read_csv(file,
    header=None,
    names=col_names,
    delimiter=' ',
    skipinitialspace=True,
    on_bad_lines = 'skip',
    usecols = col_names)

    # get rid of # character in the Sun column
    weather['Sun']=weather['Sun'].str.replace('#','')

    weather['Date']=pd.to_datetime(weather['Year']  + weather['Month'], format='%Y%m',errors='coerce')

    # change the types in the columns that should be numeric.
    weather['Year']=pd.to_numeric(weather['Year'], errors='coerce')
    weather['Month']=pd.to_numeric(weather['Month'], errors='coerce')
    weather['Tmax']=pd.to_numeric(weather['Tmax'], errors='coerce')
    weather['Tmin']=pd.to_numeric(weather['Tmin'], errors='coerce')
    weather['AF']=pd.to_numeric(weather['AF'], errors='coerce')
    weather['Rain']=pd.to_numeric(weather['Rain'], errors='coerce')
    weather['Sun']=pd.to_numeric(weather['Sun'], errors='coerce')

    # drop rows with null values in the year column to remove non data rows
    weather=weather.dropna(subset=['Year'])

    # change year and month to integers
    weather=weather.astype({'Year':'int32','Month':'int32'})

    return weather


################################## Layout ##################################################33


st.set_page_config(layout = 'wide')

# select a station name
s = st.selectbox('station', station_names)

# get the index of the station name and make the dataframe
i = station_names.index(s)
weather = makedf(i).dropna(subset=['Tmax','Tmin','Rain','Sun','AF'])

# this?
#st.dataframe(weather)


years = weather.Year.unique()
years = years[:-1] # drop 2022 as it is not complete


def makeYr(df,y):
    Tmax = df[df.Year == y].Tmax.max()
    Tmin = df[df.Year == y].Tmin.min()
    sun = df[df.Year == y].Sun.sum()
    rain = df[df.Year == y].Rain.sum()
    af = df[df.Year == y].AF.sum()
    return {'Year':y,'Tmax': Tmax, 'Tmin':Tmin, 'Sun':sun, 'Rain':rain, 'AF':af}

hist = [makeYr(weather,y) for y in years]
histdf = pd.DataFrame(hist)
#st.dataframe(histdf)



fig = px.scatter(histdf, x='Year', y='Sun', title=station_names[i], trendline='ols')
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(histdf, x='Year', y='Rain', title=station_names[i], trendline='ols')
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(histdf, x='Year', y='AF', title=station_names[i], trendline='ols')
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(histdf, x='Year', y='Tmax', title=station_names[i], trendline='ols')
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(histdf, x='Year', y='Tmin', title=station_names[i], trendline='ols')
st.plotly_chart(fig, use_container_width=True)