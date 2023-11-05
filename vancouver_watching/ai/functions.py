from abcli import file
import os
from tqdm import tqdm
import json
from vancouver_watching.ai.classes import Ultralytics_API
from vancouver_watching.ai import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def infer(
    metadata_filename: str,
    model_id: str,
    do_dryrun: bool = False,
    verbose: bool = False,
):
    success, metadata = file.load_json(metadata_filename)
    if not success:
        return False
    logger.info(
        "{}.infer: {} image(s) from {}".format(
            NAME,
            len(metadata),
            metadata_filename,
        )
    )

    ultralytics_api = Ultralytics_API(model_id, do_dryrun, verbose)

    object_path = file.path(metadata_filename)
    for image_filename in tqdm(metadata):
        metadata[image_filename]["response"] = ultralytics_api.infer(
            os.path.join(object_path, image_filename)
        )

    return file.save_json(metadata_filename, metadata)
