from .events.earthquakes import update_earthquakes
from .events.fires import update_fires
from .events.storms import update_storms
from .events.tsunamis import update_tsunamis

import arcgis
import time
import yaml
import os

with open('../config.yaml', 'r') as stream:
    config = yaml.load(stream)

gis = arcgis.GIS(username=os.environ.get('AGOL_USERNAME'),
                 password=os.environ.get('AGOL_PASSWORD'))

if __name__ == '__main__':
    while True:
        update_earthquakes(config['bbox'], config['urls']['USGS'],
                           config['translations']['earthquakes'], gis,
                           config['item_ids']['earthquakes'])
        update_fires(config['bbox'],
                     {k: config['urls'][k] for k in ['MODIS', 'VIIRS']},
                     config['translations']['fires'], gis,
                     config['item_ids']['fires'])
        update_storms(config['bbox'], config['translations']['storms'],
                      gis, config['item_ids']['storms'])
        update_tsunamis(config['bbox'], config['urls']['NOAA'],
                        config['translations']['tsunamis'], gis,
                        config['item_ids']['tsunamis'])
        time.sleep(5 * 60)
