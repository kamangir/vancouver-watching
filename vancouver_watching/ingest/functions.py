import os
import os.path
from tqdm import tqdm
from abcli import file
from . import NAME
from vancouver_watching.discover import get_list_of_cameras
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_from_cameras(filename):
    success, list_of_cameras = get_list_of_cameras(filename)
    if not success:
        return False

    success = True
    for url in tqdm(list_of_cameras):
        if not file.download(
            url,
            os.path.join(
                os.getenv("abcli_object_path"),
                file.name_and_extension(url),
            ),
        ):
            success = False

    return success
