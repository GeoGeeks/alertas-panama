from selenium import webdriver
import pandas as pd
import arcgis


def update_tsunamis(bbox, url, translation, gis, itemid):
    """
    Updates a hosted FeatureLayer in ArcGIS Online using tsunami data from
    a specified url.
    :param bbox:            Bounding box to filter the results.
    :param url:             Url to get the data from.
    :param translation:     Map to change DataFrame column names.
    :param gis:             gis object from the ArcGIS API.
    :param itemid:          Target FeatureLayer's item id.
    :return:                None.
    """
    driver = webdriver.Firefox()
    driver.get(url)
    table = driver.find_element_by_id('myTable')
    table_html = table.get_attribute('outerHTML')
    df = pd.read_html(table_html)[0]
    driver.close()
    df['Lat'] = df['Lat'].apply(lambda y: float(y[:-3]) if y[-1] == 'N' else -float(y[:-3]))
    df['Lon'] = df['Lon'].apply(lambda x: float(x[:-4]) if x[-1] == 'E' else -float(x[:-4]))
    query = f'{bbox[0]} <= Lon <= {bbox[2]} & ' \
            f'{bbox[1]} <= Lat <= {bbox[3]}'
    df.query(query, inplace=True)
    if not df.empty:
        df = df[list(translation.keys())]
        df = df.rename(columns=translation)
        lyr = gis.content.get(itemid).layers[0]
        features = lyr.query()
        ids = ','.join([str(feat.attributes['OBJECTID']) for feat in features])
        if ids:
            lyr.edit_features(deletes=ids)
        sdf = arcgis.features.SpatialDataFrame.from_xy(df.copy(), 'lon', 'lat')
        fset = arcgis.features.FeatureSet.from_dataframe(sdf)
        lyr.edit_features(adds=fset)
        print(f'Tusnami alerts updated:\t{len(fset)} added and {len(features)}'
              f' removed.')
    else:
        print('No tsunami alerts have been found.')
