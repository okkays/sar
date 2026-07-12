import gpx
import asf_search
import os
import shutil
import logging

logger = logging.getLogger('asf_gpx')


def search_for(polygon, maxResults=1, **search_kwargs):
  params = {
      'intersectsWith': polygon,
      'dataset': asf_search.DATASET.SENTINEL1,
      **search_kwargs,
  }
  count = asf_search.search_count(**params)
  log_count = logger.debug if count < 10 else logger.warning
  log_count(f'There are a total of {count} products. Fetching at most 10.')
  return asf_search.geo_search(**params, maxResults=maxResults)


def search_for_gpx(path_to_gpx, **search_kwargs):
  bounds = gpx.get_bounds(path_to_gpx)
  polygon = gpx.get_wkt_polygon(bounds)
  return search_for(polygon, **search_kwargs)


def make_session():
  try:
    with open('token.secret', 'r') as token_file:
      token = token_file.read().strip()
  except Exception as e:
    raise RuntimeError(
        'Fill out the token secret (generate a token on https://urs.earthdata.nasa.gov/) and place it in token.secret') from e
  session = asf_search.ASFSession()
  session.auth_with_token(token)
  return session


if __name__ == "__main__":
  results = search_for_gpx(
      'sample.gpx',
      processingLevel='METADATA_SLC',
      start='2 months ago',
      end='now',
      maxResults=2)

  logger.debug(results)

  xml_for_demo = results.find_urls(pattern='.*.iso.xml$')
  logger.info(f'Found results for GPX, attempting to download: {xml_for_demo}')

  shutil.rmtree('asf_data/demo')
  os.mkdir('asf_data/demo')

  asf_search.download_urls(xml_for_demo, 'asf_data/demo', session=make_session())
  logger.info('Downloaded xml to asf_data')
  logger.debug(os.listdir('asf_data/demo'))
