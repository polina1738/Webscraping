# import packages
import requests
import pandas as pd

# get weather function


def get_weather_forecast(city):
    url = "https://api.weatherapi.com/v1/current.json"
    params = {'key': "3c459a33e44044b2b86105812251304", 'q': city}
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


# define cities
cities = ['London', 'New York', 'Paris']


# get weather for each city
all_weather = [get_weather_forecast(city) for city in cities]

# assign to dataframe
weather_df = pd.json_normalize(all_weather)
weather_df = weather_df[['location.name', 'current.temp_c', 'current.feelslike_c', 'current.wind_kph',
                         'current.wind_dir', 'current.pressure_mb', 'current.humidity', 'current.cloud', 'current.uv']]

# Remove 'current.' and 'location.' prefixes from column names
weather_df.columns = [col.replace('current.', '').replace(
    'location.', '') for col in weather_df.columns]

weather_df = weather_df.rename(columns={'name': 'City', 'temp_c': 'Temperature (Celsius)', 'feelslike_c': 'Feels Like (Celsius)', 'wind_kph': 'Wind Speed (km/h)',
                               'wind_dir': 'Wind Direction', 'pressure_mb': 'Pressure (mb)', 'humidity': 'Humidity (%)', 'cloud': 'Cloud Cover (%)', 'uv': 'UV Index'})

# Read the template file
with open('api-project/templates/weather_template.html', 'r') as f:
    template = f.read()

# Replace the table placeholder with the actual table
html = template.replace('{{ table }}', weather_df.to_html(index=False))

# Save the HTML to a file
with open('api-project/weather_report.html', 'w') as f:
    f.write(html)

print("Weather report has been saved as 'api-project/weather_report.html'")
