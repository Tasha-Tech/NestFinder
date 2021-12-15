import geopandas as gpd
import utils

def load(path: str):
    # Files cloned from https://github.com/NewtonMAGIS/GISData.git
    addresses = gpd.read_file(f'{path}/addresses.geojson')
    print('Available columns', list(addresses.columns))

    # Project only relevant columns
    a = addresses[['Number', 'StreetName', 'ZipCode', 'AddressTyp', 'geometry']]
    print(f'We have {a.shape[0]} addresses in Newton')
    print(a.head(5))
    return a


def web_load(path: str):
    url = 'https://raw.githubusercontent.com/NewtonMAGIS/GISData/master/Addresses/Addresses.geojson'
    print('Loading:', url)
    data = utils.download_url(url)
    with open(f'{path}/addresses.geojson', 'w') as outfile:
        outfile.write(data)


if __name__ == "__main__":
    #  web_load('downloads')
    a = load('downloads')
