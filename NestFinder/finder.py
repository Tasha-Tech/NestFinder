import pandas as pd
from sqlalchemy import create_engine

import address
import schools
import on_sale


def meters_to_miles(meters):
    return meters * 0.000621371


def test():
    s = schools.load('downloads')
    # a = address.load('downloads')

    #  https://www.w3.org/2015/spatial/wiki/Coordinate_Reference_Systems
    #  Distance may be invalid for a geographic CRS using degrees as units
    #  Using GeoSeries.to_crs() to project geometries to a planar CRS before using geopandas.GeoSeries.distance
    if 'Geographic' in s.crs.type_name:
        s = s.to_crs(3857)

    houses = on_sale.from_disk('downloads').to_crs(3857)

    print(s['TYPE'].unique())
    for school_type in s['TYPE'].unique():
        st = s[s['TYPE'] == school_type]
        # Very interesting article about performance of row iterations
        # https://towardsdatascience.com/apply-function-to-pandas-dataframe-rows-76df74165ee4
        houses[school_type+'_school'] = pd.Series([meters_to_miles(st.distance(p).min()) for p in houses.geometry])

    print(list(houses.columns))

    # Create an in-memory SQLite database.
    sql_engine = create_engine('sqlite://', echo=False)
    sql_columns = ['address', 'listPrice', 'lotSize', 'yearBuilt']
    [sql_columns.append(col+'_school') for col in s['TYPE'].unique()]
    houses[sql_columns].to_sql('on_sale', con=sql_engine)
    report = sql_engine.execute("SELECT address, listPrice, Middle_school FROM on_sale WHERE Middle_school < 0.4").fetchall()
    print(*report, sep='\n')
    print(f'Found {len(report)} matching records')


if __name__ == "__main__":
    test()
