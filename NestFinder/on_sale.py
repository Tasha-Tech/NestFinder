from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import geopandas
from typing import Union


def download_url(url):
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 ' \
            'Safari/537.36 '

    headers = {'User-Agent': agent}
    return requests.get(url, headers=headers).text


def get_page_data(soup: BeautifulSoup, tag: str, key: str) -> Union[str, None]:
    for script in soup.find_all(tag):
        if key in script.text:
            for line in script.text.split('\n'):
                if key in line:
                    return line.split(key)[1]
    return None


def web_load(path: str):
    base_url = 'https://www.movoto.com/newton-ma/'
    counter = 0
    for loc in ['', 'p-2/', 'p-3/', 'p-4/']:
        url = base_url + loc
        print('Loading:', url)
        html = download_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        data = get_page_data(soup, 'script', 'window.__INITIAL_STATE__ = ')
        data = json.loads(data[:-1])  # Omit ';' from the end of string
        with open(f'{path}/on_sale_{counter}.json', 'w') as outfile:
            json.dump(data, outfile)

        counter += 1


def from_disk(path: str) -> geopandas.geodataframe.GeoDataFrame:
    data = None
    with open(f'{path}/on_sale_0.json', 'r') as infile:
        data = json.load(infile)

    listings = data['pageData']['listings']
    # print(json.dumps(listings[0], indent=8))
    columns = ['listPrice', 'lotSize', 'sqftTotal', 'bath', 'bed', 'propertyType', 'yearBuilt', 'zipCode']
    geo_columns = ['address', 'lat', 'lng']

    # Create dictionary with both columns
    d = dict()
    for col in columns + geo_columns:
        d[col] = list()

    for house in listings:
        for col in columns:
            d[col].append(house[col])

        for col in geo_columns:
            d[col].append(house['geo'][col])

    df = pd.DataFrame(d)
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lng, df.lat))
    gdf.set_crs(crs='epsg:4326', inplace=True)
    return gdf


if __name__ == "__main__":
    # web_load('downloads')
    from_disk('downloads')

