import os
import os.path
import re
from tqdm import tqdm
from abcli import file
from vancouver_watching.discover import get_list_of_cameras
from vancouver_watching.ingest import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_from_cameras(
    cameras_filename: str,
    count: int,
    do_dryrun: bool = False,
):
    success, list_of_cameras = get_list_of_cameras(cameras_filename)
    if not success:
        return False

    if count != -1:
        list_of_cameras = list_of_cameras[:count]
    logger.info(
        "{}.ingest_from_cameras: loaded {} camera(s) from {}.".format(
            NAME,
            len(list_of_cameras),
            cameras_filename,
        )
    )

    failed_urls = []
    p = re.compile(
        "https?:\/\/([0-9.]+).\:([0-9.]+)\/webcapture.jpg.*.channel=([0-9.]+).*"
    )
    metadata = {}
    for url in tqdm(list_of_cameras):
        matches = p.match(url)
        if matches:
            filename = (
                f"{matches[1]}-{matches[2]}-{matches[3]}".replace(".", "-") + ".jpg"
            )
        else:
            filename = file.name_and_extension(url)

        if file.extension(filename) not in "jpg,jpeg,png".split(","):
            logger.error(f"bad url: {url}.")
            failed_urls += [url]
            continue

        if do_dryrun:
            logger.info(url)
        elif not file.download(
            url,
            os.path.join(os.getenv("abcli_object_path"), filename),
        ):
            logger.error(f"bad url: {url}.")
            failed_urls += [url]
            continue

        metadata[file.name(filename)] = {"url": url}
    if failed_urls:
        logger.error("{} url(s) failed.".format(len(failed_urls)))

    metadata_filename = file.set_extension(cameras_filename, "json")
    logger.info("{} images ingested -> {}".format(len(metadata), metadata_filename))
    return file.save_json(metadata_filename, metadata)
