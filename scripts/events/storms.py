from datetime import datetime
import arcgis
import pandas as pd


def update_storms(bbox, translation, gis, itemids):
    """
    Updates a hosted FeatureLayer in ArcGIS Online using storms data from
    a specified item in the Living Atlas.
    :param bbox:            Bounding box to filter the results.
    :param translation:     Map to change DataFrame column names.
    :param gis:             gis object from the ArcGIS API.
    :param itemids:         Source and target FeatureLayers (list).
    :return:                None.
    """
    storms = gis.content.get(itemids[0]).layers[1]
    fset = storms.query()
    df = fset.df
    df['DTG'] = df['DTG'].apply(lambda x: datetime.fromtimestamp(x/1000)
                                .strftime('%Y-%m-%d%H%M'))
    df['DTG'] = pd.to_datetime(df['DTG'], format='%Y-%m-%d%H%M')
    df = df.sort_values('DTG', ascending=False).reset_index(drop=True)
    df.drop_duplicates('STORMNAME', inplace=True)
    query = f'{bbox[0]} <= LON <= {bbox[2]} & ' \
            f'{bbox[1] - 1.5} <= LAT <= {bbox[3] + 1.5}'
    df.query(query, inplace=True)
    df['STORMNAME'] = df['STORMNAME'].apply(lambda x: x.capitalize())
    df = df[list(translation.keys())]
    df = df.rename(columns=translation)
    df['fecha'] = df['fecha'].astype(str)
    lyr = gis.content.get(itemids[1]).layers[0]
    features = lyr.query()
    ids = ','.join([str(feat.attributes['OBJECTID']) for feat in features])
    if ids:
        lyr.edit_features(deletes=ids)
    sdf = arcgis.features.SpatialDataFrame.from_xy(df.copy(), 'lon', 'lat')
    fset = arcgis.features.FeatureSet.from_dataframe(sdf)
    lyr.edit_features(adds=fset)
    print(f'Storms updated:\t{len(fset)} added and {len(features)} '
          f'removed.')
