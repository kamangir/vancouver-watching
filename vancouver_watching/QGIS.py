import os
import numpy as np
from datetime import datetime
from tqdm import tqdm
from typing import Tuple
import matplotlib.pyplot as plt
from abcli.plugins.metadata import post as post_metadata, MetadataSourceType
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

    df = pd.DataFrame(
        [{"object_name": object_name_} for object_name_ in published_object_name]
    )
    for object_name_ in tqdm(published_object_name):
        filename = os.path.join(object_path, f"{object_name_}.geojson")
        if verbose:
            logger.info(f"🌀 {filename}")

        success, gdf = file.load_geodataframe(filename)
        if not success:
            continue

        added_things = []
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
                added_things += [thing]

            df.loc[df["object_name"] == object_name_, thing] = np.sum(gdf[thing].values)
        if added_things and verbose:
            logger.info(
                "+= {} thing(s): {}".format(
                    len(added_things),
                    ", ".join(added_things),
                )
            )

    list_of_things = [item for item in df.columns if item != "object_name"]
    total_counts = {thing: int(np.sum(df[thing].values)) for thing in list_of_things}
    top_things = [
        thing
        for _, thing in reversed(
            sorted(
                zip(
                    [total_counts[thing] for thing in list_of_things],
                    list_of_things,
                )
            )
        )
    ][:category_count]
    for index, thing in enumerate(top_things):
        logger.info(
            "#{}- {}: {:,g}".format(
                index,
                thing,
                total_counts[thing],
            )
        )

    dates = {
        object_name: datetime.strptime(
            "-".join(object_name.split("-")[:6]),
            "%Y-%m-%d-%H-%M-%S",
        )
        for object_name in published_object_name
    }

    plt.figure(figsize=(15, 5))
    for thing in top_things:
        plt.semilogy(
            dates.values(),
            df[thing].values,
            label=thing,
        )

    plt.xlabel("acquisition date")
    plt.ylabel("count")
    plt.grid(True)
    plt.title(object_name)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    file.save_fig(os.path.join(object_path, "counts.png"), log=True)

    return (
        post_metadata(
            "cache",
            {
                "counts": total_counts,
                "published_object_name": published_object_name,
            },
            source=object_name,
            source_type=MetadataSourceType.OBJECT,
            verbose=verbose,
        )
        and file.save_csv(
            os.path.join(object_path, "counts.csv"),
            df,
            log=True,
        ),
        df,
    )
