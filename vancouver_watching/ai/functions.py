from abcli import file
import os
from tqdm import tqdm
from abcli.modules.cookie import cookie
import json
import requests
from vancouver_watching.ai import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def run_model(
    metadata_filename: str,
    model_id: str,
    do_dryrun: bool = False,
):
    success, metadata = file.load_json(metadata_filename)
    if not success:
        return False
    logger.info(
        "{}.run_model({}): {} image(s) from {}".format(
            NAME,
            model_id,
            len(metadata),
            metadata_filename,
        )
    )

    # https://hub.ultralytics.com/models/R6nMlK6kQjSsQ76MPqQM?tab=preview
    url = f"https://api.ultralytics.com/v1/predict/{model_id}"
    logger.info(f"url: {url}")

    api_key = cookie.get("ultralytics.api.key", "")
    if not api_key:
        logger.error(
            'ultralytics.api.key not found, visit https://hub.ultralytics.com/settings?tab=api+keys, copy your API key, and then run "@cookie write ultralytics.api.key <api-key>."'
        )
        return False

    headers = {
        "x-api-key": "ab098bb19eba9b7bed2cccdc0e0a95598277303af6",
    }
    data = {
        "size": 640,
        "confidence": 0.25,
        "iou": 0.45,
    }
    path_to_images = file.path(metadata_filename)
    for image_filename in tqdm(metadata):
        if do_dryrun:
            continue

        with open(os.path.join(path_to_images, image_filename), "rb") as f:
            response = requests.post(
                url,
                headers=headers,
                data=data,
                files={"image": f},
            )

        response.raise_for_status()

        print(json.dumps(response.json(), indent=2))

    return True
