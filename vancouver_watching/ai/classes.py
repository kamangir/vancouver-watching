import cv2
from typing import Dict, Tuple, List
from abcli import file, path
from abcli.modules.cookie import cookie
from abcli.plugins.graphics import add_signature
from abcli.modules.objects import signature as object_signature
from abcli.modules.host import signature as host_signature
from vancouver_watching.ai import NAME
from vancouver_watching import VERSION
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
        render_inference: bool = True,
    ):
        self.model_id = model_id
        self.do_dryrun = do_dryrun
        self.verbose = verbose
        self.render_inference = render_inference

        self.timeout = None

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
    ) -> Tuple[bool, Dict]:
        if self.do_dryrun:
            return {}

        with open(image_filename, "rb") as f:
            response = requests.post(
                self.url,
                headers=self.headers,
                data=self.data,
                files={"image": f},
                timeout=self.timeout,
            )

        # https://chat.openai.com/c/6deb94d0-826a-48de-b5ef-f7d8da416c82
        # response.raise_for_status()
        if (
            response.status_code // 100 != 2
        ):  # Check if status code is not in the 2xx range
            logger.info(
                "{}.infer({}) failed, status_code: {}, reason: {}.".format(
                    NAME,
                    image_filename,
                    response.status_code,
                    response.reason,
                )
            )
            return False, {}

        response_dict = response.json()

        if self.verbose:
            print(json.dumps(response_dict, indent=2))

        summary = ", ".join(
            [
                "{}: {}".format(thing, count)
                for thing, count in Counter(
                    [thing["name"] for thing in response_dict["data"]]
                ).items()
            ]
        )
        logger.info(summary)

        if self.render_inference:
            file.save_image(
                file.add_postfix(
                    file.set_extension(image_filename, "jpg"), "inference"
                ),
                self.render(
                    image=file.load_image(image_filename)[1].copy(),
                    inference=response_dict,
                    header=[
                        " | ".join(
                            object_signature(
                                object_name=path.name(file.path(image_filename)),
                                info=file.name(image_filename),
                            )
                            + [summary]
                        )
                    ],
                ),
                log=True,
            )

        return True, response_dict

    @staticmethod
    def render(
        image,
        inference,
        header: List = [],
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.5,
    ):
        image = image.copy()
        for thing in inference["data"]:
            x1 = int(thing["box"]["x1"])
            y1 = int(thing["box"]["y1"])
            x2 = int(thing["box"]["x2"])
            y2 = int(thing["box"]["y2"])
            text = "{}: {:.2f}".format(thing["name"], thing["confidence"])

            image[y1:y2, x1:x2, :] = 255 - image[y1:y2, x1:x2, :]
            for thickness, color in zip([4, 1], [0, 255]):
                image = cv2.putText(
                    image,
                    text=text,
                    org=(x2, y2),
                    fontFace=fontFace,
                    fontScale=fontScale,
                    color=3 * (color,),
                    thickness=thickness,
                )

        return add_signature(
            image,
            header=header,
            footer=[
                " | ".join([f"{NAME}-{VERSION}"] + host_signature()),
            ],
        )
