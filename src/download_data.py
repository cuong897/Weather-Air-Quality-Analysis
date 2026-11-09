from datetime import datetime
from meteostat import Point, Daily
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Download weather data

Ho_Chi_Minh = Point(10.823, 106.6296)
start = datetime(2023,1,1)
end = datetime(2023,12,31)
data = Daily(Ho_Chi_Minh, start, end)
data = data.fetch() #Truy vấn, lấy kết quả chuyển từ thô -> dataFrame

data.to_csv("raw/weather_data.csv")


# Download air quality data

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
	"latitude": 10.823,
	"longitude": 106.6296,
	"hourly": ["pm10", "pm2_5", "uv_index", "uv_index_clear_sky", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "carbon_monoxide", "carbon_dioxide"],
	"timezone": "Asia/Bangkok",
	"start_date": "2023-01-01",
	"end_date": "2023-12-31",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(2).ValuesAsNumpy()
hourly_uv_index_clear_sky = hourly.Variables(3).ValuesAsNumpy()
hourly_nitrogen_dioxide = hourly.Variables(4).ValuesAsNumpy()
hourly_sulphur_dioxide = hourly.Variables(5).ValuesAsNumpy()
hourly_ozone = hourly.Variables(6).ValuesAsNumpy()
hourly_carbon_monoxide = hourly.Variables(7).ValuesAsNumpy()
hourly_carbon_dioxide = hourly.Variables(8).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["pm10"] = hourly_pm10
hourly_data["pm2_5"] = hourly_pm2_5
hourly_data["uv_index"] = hourly_uv_index
hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
hourly_data["nitrogen_dioxide"] = hourly_nitrogen_dioxide
hourly_data["sulphur_dioxide"] = hourly_sulphur_dioxide
hourly_data["ozone"] = hourly_ozone
hourly_data["carbon_monoxide"] = hourly_carbon_monoxide
hourly_data["carbon_dioxide"] = hourly_carbon_dioxide

hourly_dataframe = pd.DataFrame(data = hourly_data)
hourly_dataframe.to_csv("raw/air_quality.csv")
