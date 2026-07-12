import sys
import asf_gpx
import geo
import argparse
import logging

logger = logging.getLogger('gpx_to_sar')
logging.basicConfig(level=logging.DEBUG)


def parse_arguments():
  parser = argparse.ArgumentParser(
      description='sum the integers at the command line')
  parser.add_argument('path_to_gpx',
                      help='The GPX file for which to download products')

  return parser.parse_args()


def main():
  args = parse_arguments()
  logger.debug(f'Reading gpx file: {args.path_to_gpx}')
  results = asf_gpx.search_for_gpx(
      args.path_to_gpx,
      processingLevel='SLC',
      start='6 months ago',
      end='now',
      maxResults=10)

  geo.show_results_with_gpx(args.path_to_gpx, results.geojson())


if __name__ == "__main__":
  sys.argv = [__file__, 'sample.gpx']
  main()
