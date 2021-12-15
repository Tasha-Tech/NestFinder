import geopandas as gpd
import utils


def load(path: str):
    # Files cloned from https://github.com/NewtonMAGIS/GISData.git
    schools = gpd.read_file(f'{path}/schools.geojson')
    print('Available columns', list(schools.columns))

    # Project only relevant columns
    schools = schools[['NAME', 'ADDRESS', 'TYPE', 'geometry']]
    print(f'We have {schools.shape[0]} schools in Newton')
    return schools

def web_load(path: str):
    url = 'https://raw.githubusercontent.com/NewtonMAGIS/GISData/master/Schools/Schools.geojson'
    print('Loading:', url)
    data = utils.download_url(url)
    with open(f'{path}/schools.geojson', 'w') as outfile:
        outfile.write(data)


if __name__ == "__main__":
    # web_load('downloads')
    s = load('downloads')
