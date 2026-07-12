import json
import plotly.graph_objects as go
import plotly.express as px
import geopandas
import gpx
import shapely


def show_results_with_gpx(gpx_filename, results):
  gpx_bounds = gpx.get_bounds(gpx_filename)
  gpx_geojson = gpx.get_geojson(gpx_filename)  # TODO: don't re-read file

  df = geopandas.GeoDataFrame.from_features(results['features'])

  (min_lat, min_lon), (max_lat, max_lon) = gpx_bounds
  center = {
      'lat': (max_lat + min_lat) / 2,
      'lon': (max_lon + min_lon) / 2
  }
  fig = px.choropleth_map(df,
                          geojson=df.geometry,
                          opacity=0.2,
                          locations=df.index,
                          hover_data=[
                              'platform',
                              'pathNumber',
                              'frameNumber',
                              'processingDate',
                          ],
                          color='fileID',
                          map_style="open-street-map",
                          center=center,
                          zoom=6,
                          )

  gpx_df = geopandas.GeoDataFrame.from_features(gpx_geojson['features'])
  for feature in gpx_df.geometry:
    if isinstance(feature, shapely.geometry.linestring.LineString):
      linestrings = [feature]
    elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
      linestrings = feature.geoms
    else:
      continue
    for linestring in linestrings:
      lon, lat = linestring.xy
      gpx_line = go.Scattermap(mode='lines',
                               lon=list(lon), lat=list(lat),
                               line={'color': 'red'})
      gpx_line.name = gpx_filename
      fig.add_trace(gpx_line)

  fig.show()


if __name__ == '__main__':
  gpx_filename = 'sample.gpx'

  with open('sample_results.json', 'r') as sample_file:
    results = json.load(sample_file)

  show_results_with_gpx(gpx_filename, results)
