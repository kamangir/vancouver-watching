from abcli import file
from abcli import path
import os
from tqdm import tqdm
import json
from vancouver_watching.ai.classes import Ultralytics_API
from vancouver_watching.ai import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def infer_object(
    area: str,
    object_path: str,
    model_id: str,
    do_dryrun: bool = False,
    verbose: bool = False,
):
    metadata_filename = os.path.join(object_path, f"{area}.json")
    success, metadata = file.load_json(metadata_filename)
    if not success:
        return False
    logger.info(
        "{}.infer: {} image(s) from {}".format(
            NAME,
            len(metadata),
            path.name(object_path),
        )
    )

    ultralytics_api = Ultralytics_API(model_id, do_dryrun, verbose)

    for image_filename in tqdm(metadata):
        success, metadata[image_filename]["inference"] = ultralytics_api.infer(
            os.path.join(object_path, image_filename)
        )
        if not success:
            break

    return file.save_json(metadata_filename, metadata)


def process(
    area: str,
    object_path: str,
    model_id: str,
    do_dryrun: bool = False,
    verbose: bool = False,
):
    logger.info(
        "{}.process: {}".format(
            NAME,
            path.name(object_path),
        )
    )

    if not infer_object(
        area=area,
        object_path=object_path,
        model_id=model_id,
        do_dryrun=do_dryrun,
        verbose=verbose,
    ):
        return False

    logger.info("🪄")

    return True
