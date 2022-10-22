import os
import os.path
from tqdm import tqdm
from abcli import file
from . import NAME
from vancouver_watching.discover import discover_cameras
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_from_cameras(filename):
    list_of_cameras = discover_cameras(filename)

    logger.info(
        f"{NAME}.ingest_from_cameras({filename}): ingesting from {len(list_of_cameras)} cameras(s)."
    )

    success = True
    for camera in tqdm(list_of_cameras):
        if not file.download(
            f"https://trafficcams.vancouver.ca/{camera}",
            os.path.join(
                os.getenv("abcli_object_path"),
                file.name_and_extension(camera),
            ),
        ):
            success = False

    return success
