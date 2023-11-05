import cv2
from abcli import file
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
        render_inference: bool = True,
    ):
        self.model_id = model_id
        self.do_dryrun = do_dryrun
        self.verbose = verbose
        self.render_inference = render_inference

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

        if self.render_inference:
            file.save_image(
                file.add_postfix(
                    file.set_extension(image_filename, "jpg"), "inference"
                ),
                self.render(
                    file.load_image(image_filename)[1].copy(),
                    response_dict,
                ),
                log=True,
            )

        return response_dict

    @staticmethod
    def render(
        image,
        response_dict,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.5,
    ):
        image = image.copy()
        for thing in response_dict["data"]:
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

        return image
