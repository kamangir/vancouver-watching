import os
import os.path
from tqdm import tqdm

from blueness import module
from bluer_objects import file

from vancouver_watching import NAME
from vancouver_watching.target.classes import Target
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


def ingest_target(
    target: Target,
    count: int = -1,
) -> bool:
    logger.info("{}.ingest({})".format(NAME, count))
    counter = 0
    for mapid in tqdm(target.metadata):
        for filename, metadata in target.metadata[mapid]["cameras"].items():
            url = metadata["url"]

            if target.do_dryrun:
                logger.info(url)
            elif not file.download(
                url,
                os.path.join(
                    target.object_path,
                    filename,
                ),
            ):
                logger.error("bad url: {}.".format(url))

            counter += 1
            if counter >= count and count != -1:
                break
        if counter >= count and count != -1:
            break

    return True
