import os
import numpy as np
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
    category_count: int = 10,
    verbose: bool = False,
) -> Tuple[bool, pd.DataFrame]:
    logger.info(f"update_cache({object_name} @ {category_count})")

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
        [{"object_name": object_name_} for object_name_ in published_object_name]
    )
    for object_name_ in published_object_name:
        filename = os.path.join(object_path, f"{object_name_}.geojson")
        logger.info(f"🌀 {filename}")

        success, gdf = file.load_geodataframe(filename)
        if not success:
            continue

        for thing in gdf.columns:
            if thing in [
                "mapid",
                "url",
                "name",
                "geo_local_area",
                "cameras",
                "label",
                "geometry",
            ]:
                continue

            if thing not in list(df.columns):
                df[thing] = 0

            df.loc[df["object_name"] == object_name_, thing] = np.sum(gdf[thing].values)

    list_of_things = [item for item in df.columns if item != "object_name"]
    total_counts = {thing: np.sum(df[thing].values) for thing in list_of_things}
    list_of_counts = [total_counts[thing] for thing in list_of_things]
    top_things = [
        thing for count, thing in reversed(sorted(zip(list_of_counts, list_of_things)))
    ][:category_count]
    for index, thing in enumerate(top_things):
        logger.info(
            "#{}- {}: {:,g}".format(
                index,
                thing,
                total_counts[thing],
            )
        )

    # TODO: visualize object count per acquisition

    # TODO: save metadata

    return True, df
