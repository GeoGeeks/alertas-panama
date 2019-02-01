# alertas-panama

### Descripción
Este repositorio consiste en una serie de scripts de Python que actualizan automáticamente los servicios de ArcGIS del [Dashboard de Alertas de Eventos Naturales en Tiempo Real para Panamá](http://arcg.is/1uaby9).
Los servicios que actualizan son los siguientes:
* [Alertas de Tsunamis](https://services.arcgis.com/8DAUcrpQcpyLMznu/arcgis/rest/services/tsunamis_vista/FeatureServer)
* [Incendios Forestales](https://services.arcgis.com/8DAUcrpQcpyLMznu/arcgis/rest/services/incendios_vista/FeatureServer)
* [Terremotos](https://services.arcgis.com/8DAUcrpQcpyLMznu/arcgis/rest/services/terremotos_vista/FeatureServer)
* [Tormentas](https://services.arcgis.com/8DAUcrpQcpyLMznu/arcgis/rest/services/tormentas_vista/FeatureServer)


### Fuentes de datos
Las fuentes de datos para alimentar los servicios son las siguieentes:
* Alertas: [NOAA](https://www.tsunami.gov/)
* Incendios: [FIRMS](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data)
* Terremotos: [USGS](https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php)
* Tormentas: [Living Atlas](https://livefeeds.arcgis.com/arcgis/login/?returnUrl=https://livefeeds.arcgis.com/arcgis/rest/services/LiveFeeds/Hurricane_Active/MapServer)
* Volcanes: [Smithsonian](https://volcano.si.edu/reports_weekly.cfm)


### Contacto
En caso de cualquier duda sobre la implementación de este proyecto por favor contactar a Marcelo Villa (mvilla@esri.co).


### Licencia
MIT - <http://www.opensource.org/licenses/mit-license.php>