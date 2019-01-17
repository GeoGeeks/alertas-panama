import pandas as pd
import arcgis


def update_earthquakes(bbox, url, translation, gis, itemid):
    """
    Updates a hosted FeatureLayer in ArcGIS Online using earthquake data from
    a specified url.
    :param bbox:            Bounding box to filter the results.
    :param url:             Url to get the data from.
    :param translation:     Map to change DataFrame column names.
    :param gis:             gis object from the ArcGIS API.
    :param itemid:          Target FeatureLayer's item id.
    :return:                None.
    """
    df = pd.read_csv(url)
    query = f'{bbox[0]} <= longitude <= {bbox[2]} & ' \
            f'{bbox[1]} <= latitude <= {bbox[3]}'
    df.query(query, inplace=True)

    if not df.empty:
        df = df[list(translation.keys())]
        df = df.rename(columns=translation)
        df['fecha'] = df['fecha'].str.replace('T', ' ').str.replace('Z', ' ').str[
                      :-5]
        lyr = gis.content.get(itemid).layers[0]
        features = lyr.query()
        ids = ','.join([str(feat.attributes['OBJECTID']) for feat in features])
        if ids:
            lyr.edit_features(deletes=ids)
        sdf = arcgis.features.SpatialDataFrame.from_xy(df.copy(), 'lon', 'lat')
        fset = arcgis.features.FeatureSet.from_dataframe(sdf)
        lyr.edit_features(adds=fset)
        print(f'Earthquakes updated:\t{len(fset)} added and {len(features)} '
              f'removed.')
    else:
        print('No earthquakes have been found.')



