import os
import logging


logger = logging.getLogger(__name__)

# All video extensions
EXT = (".3g2 .3gp .3gp2 .3gpp .60d .ajp .asf .asx .avchd .avi .bik .bix"
       ".box .cam .dat .divx .dmf .dv .dvr-ms .evo .flc .fli .flic .flv"
       ".flx .gvi .gvp .h264 .m1v .m2p .m2ts .m2v .m4e .m4v .mjp .mjpeg"
       ".mjpg .mkv .moov .mov .movhd .movie .movx .mp4 .mpe .mpeg .mpg"
       ".mpv .mpv2 .mxf .nsv .nut .ogg .ogm .omf .ps .qt .ram .rm .rmvb"
       ".swf .ts .vfw .vid .video .viv .vivo .vob .vro .wm .wmv .wmx"
       ".wrap .wvx .wx .x264 .xvid")
EXT = tuple(EXT.split())


def scan_video(path):
    """Scan a video from a video `path`.

    :param string path: absolute path to the video
    """

    if os.path.getsize(path) < (25 * 10124 * 1024):
        raise ValueError("Size less than 25 MB")

    # Todo: Should some processing happen here?
    return path


def scan_videos(paths):
    """Scan `paths` for videos.

    :params paths: absolute paths to scan for videos
    :type paths: list of string
    :return: the scanned videos
    :rtype: list of :class:`Video`

    """
    videos = []

    # scan files
    for filepath in [p for p in paths if os.path.isfile(p)]:
        try:
            videos.append(scan_video(filepath))
        except ValueError as e:
            logger.error('Skipping video %s: %s', (filepath, e))
            continue

    # scan directories
    for path in [p for p in paths if os.path.isdir(p)]:

        logger.info('Scanning directory %r', path)

        for dirpath, dirnames, filenames in os.walk(path):

            # skip hidden sub directories
            for dirname in list(dirnames):
                if dirname.startswith('.'):
                    logger.debug('Skipping hidden dirname %r in %r', dirname, dirpath)
                    dirnames.remove(dirname)

            # scan for videos
            for filename in filenames:

                # filter videos
                if not filename.endswith(EXT):
                    continue

                # skip hidden files
                if filename.startswith('.'):
                    logger.debug('Skipping hidden filename %r in %r', filename, dirpath)
                    continue

                filepath = os.path.join(dirpath, filename)

                # skip links
                if os.path.islink(filepath):
                    logger.debug('Skipping link %r in %r', filename, dirpath)
                    continue

                try:
                    video = scan_video(filepath)
                except ValueError as e:
                    logger.error('Skipping video %s: %s', filepath, e)
                    continue
                videos.append(video)

    return videos
