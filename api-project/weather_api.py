#import packages
import requests
import pandas as pd

#
def get_weather_forecast(city):
    url = "https://api.weatherapi.com/v1/current.json"
    params = {'key': "3c459a33e44044b2b86105812251304",'q': city}
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


cities = ['London', 'New York', 'Paris']
    
all_weather = [get_weather_forecast(city) for city in cities]

df = pd.json_normalize(all_weather)

df.set_index('location.name', inplace = True)
print(df.loc['London', 'current.temp_c'])

