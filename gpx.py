import gpxpy

def get_sample_bounds():
    with open('sample.gpx', 'r') as sample:
        gpx = gpxpy.parse(sample)

    bounds = gpx.get_bounds()
    return (bounds.min_latitude, bounds.min_longitude), (bounds.max_latitude, bounds.max_longitude)

if __name__ == "__main__":
    bounds = get_sample_bounds()
    print(bounds)

