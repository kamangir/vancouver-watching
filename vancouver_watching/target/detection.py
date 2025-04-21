import os
import os.path
from typing import List
import re
from collections import Counter
from tqdm import tqdm

from blueness import module
from bluer_objects import file
from bluer_objects.graphics.gif import generate_animated_gif

from vancouver_watching import NAME
from vancouver_watching.ai import Ultralytics_API
from vancouver_watching.target.classes import Target
from vancouver_watching.logger import logger


NAME = module.name(__file__, NAME)


def detect_in_target(
    target: Target,
    model_id: str,
    animated_gif: bool = False,
    count: int = -1,
    overwrite: bool = False,
) -> bool:
    logger.info(
        "{}.detect_in_target(model_id={},count={}){}{}".format(
            NAME,
            model_id,
            count,
            " +animated_gif" if animated_gif else "",
            " +overwrite" if overwrite else "",
        )
    )

    ultralytics_api = Ultralytics_API(
        model_id,
        target.do_dryrun,
        target.verbose,
    )

    list_of_images: List[str] = []
    counter: int = 0
    all_detections = {}
    for mapid in tqdm(target.metadata):
        detections = {}
        for filename, metadata in target.metadata[mapid]["cameras"].items():
            full_filename = os.path.join(target.object_path, filename)
            if not file.exists(full_filename):
                continue

            if target.do_dryrun:
                logger.info(f"dryrun: skipping {full_filename} ...")
                continue

            if overwrite or "inference" not in metadata:
                success, inference = ultralytics_api.infer(full_filename)
                if success:
                    metadata["inference"] = inference
                    list_of_images += [inference.get("render_filename", "")]

            if "inference" not in metadata:
                continue

            for thing, thing_count in Counter(
                [
                    thing["name"]
                    for thing in metadata["inference"]["images"][0]["results"]
                ]
            ).items():
                detections[thing] = detections.get(thing, 0) + thing_count

            if detections:
                logger.info(
                    "{}: {}".format(
                        mapid,
                        " + ".join(
                            [
                                f"{thing_count}*{thing}"
                                for thing, thing_count in detections.items()
                            ]
                        ),
                    )
                )

            for thing, thing_count in detections.items():
                all_detections[thing] = all_detections.get(thing, 0) + thing_count

                if thing not in target.gdf.columns:
                    target.gdf[thing] = 0
                    logger.info("+= {}".format(thing))

                target.gdf.loc[target.gdf["mapid"] == mapid, thing] += thing_count

            counter += 1
            if count != -1 and counter >= count:
                break
        if count != -1 and counter >= count:
            break

    logger.info(
        "all: {}".format(
            " + ".join(
                [
                    f"{thing_count}*{thing}"
                    for thing, thing_count in all_detections.items()
                ]
            )
        )
    )

    if not target.save_metadata():
        return False

    if not target.save_gdf():
        return False

    return not animated_gif or generate_animated_gif(
        [filename for filename in list_of_images if filename],
        os.path.join(target.object_path, f"{target.object_name}.gif"),
        frame_duration=500,
    )
