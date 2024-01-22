import os
from datetime import datetime
from typing import Tuple
import pandas as pd
import glob
from abcli import file
from abcli.modules import objects
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def label_of_camera(
    location_url,
    location_name,
    list_of_cameras,
):
    return '<a href="{}">{}</a><br/> {}'.format(
        location_url,
        location_name,
        f'<img src="{list_of_cameras[0]}">' if list_of_cameras else "camera not found.",
    )


def update_cache(
    object_name: str = ".",
    verbose: bool = False,
) -> Tuple[bool, pd.DataFrame]:
    logger.info(f"update_cache({object_name})")

    object_path = objects.object_path(object_name, create=True)

    published_object_name = sorted(
        [
            file.name(filename)
            for filename in glob.glob(os.path.join(object_path, "*.geojson"))
        ]
    )
    logger.info(
        "🌀 {} published object(s) found{}".format(
            len(published_object_name),
            ": {}".format(", ".join(published_object_name)) if verbose else ".",
        )
    )

    dates = {
        object_name: datetime.strptime(
            "-".join(object_name.split("-")[:6]),
            "%Y-%m-%d-%H-%M-%S",
        )
        for object_name in published_object_name
    }

    df = pd.DataFrame(
        [
            {"object_name": object_name_, "total": 0}
            for object_name_ in published_object_name
        ]
    )

    for object_name_ in published_object_name:
        filename = os.path.join(object_path, f"{object_name_}.geojson")
        logger.info(f"🌀 {filename}")

        success, gdf = file.load_geodataframe(filename)
        if not success:
            continue

        detected_things = [
            item
            for item in gdf.columns
            if item
            not in [
                "mapid",
                "url",
                "name",
                "geo_local_area",
                "cameras",
                "label",
                "geometry",
            ]
            + list(df.columns)
        ]
        for thing in detected_things:
            if verbose:
                logger.info(f"+= {thing}")
            df[thing] = 0

        break

    # TODO: object count per acquisition

    return True, df
