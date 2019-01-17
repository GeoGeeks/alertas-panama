import pandas as pd
import arcgis


def update_fires(bbox, urls, translation, gis, itemid):
    """
    Updates a hosted FeatureLayer in ArcGIS Online using fire data from
    a specified url.
    :param bbox:            Bounding box to filter the results.
    :param url:             Urls to get the data from (dict).
    :param translation:     Map to change DataFrame column names.
    :param gis:             gis object from the ArcGIS API.
    :param itemid:          Target FeatureLayer's item id.
    :return:                None.
    """
    cols = ['lon', 'lat', 'fecha', 'satelite']
    df = pd.DataFrame(columns=cols)
    for sat in urls.keys():
        fires = pd.read_csv(urls[sat])
        query = f'{bbox[0]} <= longitude <= {bbox[2]} & ' \
                f'{bbox[1]} <= latitude <= {bbox[3]}'
        # if sat == 'MODIS':
        #     query += ' & confidence >= 75'
        # else:
        #     query += ' & confidence == "high"'
        fires = fires.query(query).reset_index(drop=True)
        fires['dt'] = fires['acq_date'].str.cat(fires['acq_time'].astype(str))
        fires['dt'] = pd.to_datetime(fires['dt'], format='%Y-%m-%d%H%M')
        fires = fires.rename(columns=translation)
        fires = fires[cols[:-1]]
        df = df.append(fires, ignore_index=True, sort=False)
        df['satelite'].fillna(sat, inplace=True)

    if not df.empty:
        lyr = gis.content.get(itemid).layers[0]
        features = lyr.query()
        ids = ','.join([str(feat.attributes['OBJECTID']) for feat in features])
        if ids:
            lyr.edit_features(deletes=ids)
        df['fecha'] = df['fecha'].astype(str)
        sdf = arcgis.features.SpatialDataFrame.from_xy(df.copy(), 'lon', 'lat')
        fset = arcgis.features.FeatureSet.from_dataframe(sdf)
        lyr.edit_features(adds=fset)
        print(f'Fires updated:\t{len(fset)} added and {len(features)} '
              f'removed.')
    else:
        print('No fires have been found.')





