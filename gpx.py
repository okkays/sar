import gpxpy


def get_geojson(path_to_gpx):
  with open(path_to_gpx, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

  return {
      'features': [
          {
              'geometry': {
                  'type': 'LineString',
                  'coordinates': [
                      [point.longitude, point.latitude]
                      for point in segment.points
                  ]
              },
              'properties': {}
          }
          for track in gpx.tracks for segment in track.segments
      ]
  }


def get_bounds(path_to_gpx):
  with open(path_to_gpx, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

  bounds = gpx.get_bounds()
  return (bounds.min_latitude, bounds.min_longitude), (bounds.max_latitude, bounds.max_longitude)


def get_geojson_polygon(bounds):
  (min_lat, min_lon), (max_lat, max_lon) = bounds
  return {
      'geometry': {
          'coordinates': [
              [min_lon, min_lat],
              [max_lon, min_lat],
              [max_lon, max_lat],
              [min_lon, max_lat],
              [min_lon, min_lat],
          ]
      },
      'type': 'Polygon'
  }


def get_wkt_polygon(bounds):
  (min_lat, min_lon), (max_lat, max_lon) = bounds
  corners = ((min_lon, min_lat),
             (max_lon, min_lat),
             (max_lon, max_lat),
             (min_lon, max_lat),
             (min_lon, min_lat))  # Repeat corner 1 to close the loop

  formatted_corners = ','.join([' '.join([str(p) for p in c]) for c in corners])
  return f'POLYGON(({formatted_corners}))'


if __name__ == "__main__":
  geojson = get_geojson('sample.gpx')
  print(geojson)

  bounds = get_bounds('sample.gpx')
  print(bounds)
