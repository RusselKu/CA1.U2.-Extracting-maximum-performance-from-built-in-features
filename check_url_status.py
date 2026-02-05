import requests

url = "https://www.ncei.noaa.gov/data/global-hourly/access/2021/01044099999.csv"
response = requests.head(url)
print(f"URL: {url}")
print(f"Status Code: {response.status_code}")