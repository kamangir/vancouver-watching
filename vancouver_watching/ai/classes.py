from abcli.modules.cookie import cookie
import requests
from collections import Counter
import json
from abcli import logging
import logging

logger = logging.getLogger(__name__)


class Ultralytics_API(object):
    def __init__(
        self,
        model_id: str,
        do_dryrun: bool = False,
        verbose: bool = False,
    ):
        self.model_id = model_id
        self.do_dryrun = do_dryrun
        self.verbose = verbose

        # https://hub.ultralytics.com/models/R6nMlK6kQjSsQ76MPqQM?tab=preview
        self.url = f"https://api.ultralytics.com/v1/predict/{self.model_id}"
        logger.info(f"{self.__class__.__name__}.url: {self.url}")

        self.valid = True
        self.api_key = cookie.get("ultralytics.api.key", "")
        if not self.api_key:
            logger.error(
                'ultralytics.api.key not found, visit https://hub.ultralytics.com/settings?tab=api+keys, copy your API key, and then run "@cookie write ultralytics.api.key <api-key>."'
            )
            self.valid = False

        self.headers = {
            "x-api-key": self.api_key,
        }
        self.data = {
            "size": 640,
            "confidence": 0.25,
            "iou": 0.45,
        }

    def infer(
        self,
        image_filename: str,
    ):
        if self.do_dryrun:
            return {}

        with open(image_filename, "rb") as f:
            response = requests.post(
                self.url,
                headers=self.headers,
                data=self.data,
                files={"image": f},
            )

        response.raise_for_status()

        response_dict = response.json()

        if self.verbose:
            print(json.dumps(response_dict, indent=2))

        logger.info(
            ", ".join(
                [
                    "{}: {}".format(thing, count)
                    for thing, count in Counter(
                        [thing["name"] for thing in response_dict["data"]]
                    ).items()
                ]
            )
        )

        return response_dict
