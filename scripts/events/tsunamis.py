from selenium import webdriver
import pandas as pd
import arcgis


def update_tsunamis(bbox, url, translation, gis, itemid):
    """

    :param bbox:
    :param url:
    :param translation:
    :param gis:
    :param itemid:
    :return:
    """
    driver = webdriver.Firefox()
    driver.get(url)
    table = driver.find_element_by_id('myTable')
    table_html = table.get_attribute('outerHTML')
    df = pd.read_html(table_html)[0]
    df['Lat'] = df['Lat'].apply(lambda y: float(y[:-3]) if y[-1] == 'N' else -float(y[:-3]))
    df['Lon'] = df['Lon'].apply(lambda x: float(x[:-4]) if x[-1] == 'E' else -float(x[:-4]))
    query = f'{bbox[0]} <= Lon <= {bbox[2]} & ' \
            f'{bbox[1]} <= Lat <= {bbox[3]}'
    df.query(query, inplace=True)
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
    driver.close()
