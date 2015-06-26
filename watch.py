import os
import json
from shutil import copy
import logging

# Todo: Remove dependency on omdb module and
# use the api directly?
from urllib import urlopen, urlencode

from guessit import guess_file_info

from scanner import scan_videos

# Disable logging for scanner
logger = logging.getLogger("scanner")
logger.addHandler(logging.NullHandler())

# Enable for this file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


OMDB_URL = 'http://www.omdbapi.com/?'


def omdb(title, year=None):
    """ Fetch data from OMDB API. """
    params = {'t': title, 'plot': 'full', 'type': 'movie', 'tomatoes': 'true'}
    if year:
        params['y'] = year

    url = OMDB_URL + urlencode(params)
    logger.info('\033[33m' + "Fetching URL: %s" % url + '\033[0m')

    data = json.load(urlopen(url))

    # Todo: Handle errors?
    if data['Response'] == 'False':
        data = None

    return data, url


def get_movie_info(path):
    """Find movie information from a `path` to file."""

    # Use the guessit module to find details of a movie from name
    file = guess_file_info(os.path.basename(path))

    # Use omdb to find ratings, genre etc. from title and year
    data, url = omdb(file['title'], file.get('year'))

    return data


if __name__ == '__main__':
    videos = scan_videos(["/mnt/Entertainment/Movies"])

    for video_path in videos:

        logger.info("Processing: %s" % video_path)

        movie_json = video_path + ".json"

        try:
            with open(movie_json) as inp:
                info = json.load(inp)

        except IOError, e:
            info = get_movie_info(video_path)

            if not info:
                logger.error('\033[31m' + "No info found for: %s" % video_path + '\033[0m')
                continue

            with open(movie_json, "w") as out:
                json.dump(info, out, indent=2)

        # Copy these movie-data files to a folder
        # so I can have a list of all installed movies :)
        file = "%s - %s.json" % (info["year"], info["title"])
        copy(movie_json, os.path.expanduser("~/Movies/%s" % file))

        # Group the movies according to categories and sort the categories
        # according to ratings

        # You can now do shit like 'Play the best comedy movie I have.'
