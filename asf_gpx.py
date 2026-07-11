import gpx
import asf_search
import os
import shutil
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('asf_gpx')

def get_polygon(bounds):
    (min_lat, min_lon), (max_lat, max_lon) = bounds
    corners = ((min_lon, min_lat),
               (max_lon, min_lat),
               (max_lon, max_lat),
               (min_lon, max_lat),
               (min_lon, min_lat))  # Repeat corner 1 to close the loop

    formatted_corners = ','.join([' '.join([str(p) for p in c]) for c in corners])
    return f'POLYGON(({formatted_corners}))'

def search_for(polygon, maxResults=1, **search_kwargs):
    params = {
        'intersectsWith': polygon,
        'dataset': asf_search.DATASET.SENTINEL1,
        'start': '2 months ago',
        'end': 'now',
        **search_kwargs,
    }
    count = asf_search.search_count(**params)
    log_count = logger.debug if count < 10 else logger.warning
    log_count(f'There are a total of {count} products. Fetching at most 10.')
    return asf_search.geo_search(**params, maxResults=maxResults)

def make_session():
    try:
        with open('token.secret', 'r') as token_file:
            token = token_file.read().strip()
    except Exception as e:
        raise RuntimeError('Fill out the token secret (generate a token on https://urs.earthdata.nasa.gov/) and place it in token.secret') from e
    session = asf_search.ASFSession()
    session.auth_with_token(token)
    return session

if __name__ == "__main__":
    sample_bounds = gpx.get_sample_bounds()
    sample_polygon = get_polygon(sample_bounds)
    results = search_for(sample_polygon,
                         processingLevel='METADATA_SLC',
                         maxResults=2)

    logger.debug(results)

    xml_for_demo = results.find_urls(pattern='.*.iso.xml$')
    logger.info(f'Found results for GPX, attempting to download: {xml_for_demo}')

    shutil.rmtree('asf_data/demo')
    os.mkdir('asf_data/demo')

    asf_search.download_urls(xml_for_demo, 'asf_data/demo', session=make_session())
    logger.info('Downloaded xml to asf_data')
    logger.debug(os.listdir('asf_data/demo'))
