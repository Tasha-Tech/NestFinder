import pandas as pd
import geopandas as gpd


def load():
    # Files cloned from https://github.com/NewtonMAGIS/GISData.git
    addresses = gpd.read_file('../GISData/Addresses/Addresses.geojson')
    print('Available columns', list(addresses.columns))

    # Project only relevant columns
    a = addresses[['Number', 'StreetName', 'ZipCode', 'AddressTyp', 'geometry']]
    print(f'We have {a.shape[0]} addresses in Newton')
    print(a.head(5))
    return a


if __name__ == "__main__":
    a = load()
