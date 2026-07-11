import gpxpy


def get_bounds(path_to_gpx):
  with open(path_to_gpx, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

  bounds = gpx.get_bounds()
  return (bounds.min_latitude, bounds.min_longitude), (bounds.max_latitude, bounds.max_longitude)


if __name__ == "__main__":
  bounds = get_bounds('sample.gpx')
  print(bounds)
