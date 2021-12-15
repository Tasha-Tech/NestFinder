import pandas as pd
import geopandas as gpd


def load():
    # Files cloned from https://github.com/NewtonMAGIS/GISData.git
    schools = gpd.read_file('../GISData/Schools/Schools.geojson')
    print('Available columns', list(schools.columns))

    # Project only relevant columns
    s = schools[['NAME', 'ADDRESS', 'TYPE', 'geometry']]
    print(f'We have {s.shape[0]} schools in Newton')
    return s


if __name__ == "__main__":
    s = load()
