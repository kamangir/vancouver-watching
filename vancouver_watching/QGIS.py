import os
import numpy as np
from datetime import datetime
from tqdm import tqdm
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd
import glob

from blueness import module
from blue_options import fullname
from blue_objects import file, objects
from blue_objects.metadata import post_to_object

from vancouver_watching import NAME, VERSION
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


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
    logger.info(f"update_cache({object_name} @ {category_count} categories)")

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
                df[thing] = 0.0
                added_things += [thing]

            df.loc[df["object_name"] == object_name_, thing] = np.mean(
                gdf[thing].values
            )
        if added_things and verbose:
            logger.info(
                "+= {} thing(s): {}".format(
                    len(added_things),
                    ", ".join(added_things),
                )
            )

    list_of_things = [item for item in df.columns if item != "object_name"]
    mean_counts = {thing: float(np.mean(df[thing].values)) for thing in list_of_things}
    top_things = [
        thing
        for _, thing in reversed(
            sorted(
                zip(
                    [mean_counts[thing] for thing in list_of_things],
                    list_of_things,
                )
            )
        )
    ][:category_count]
    for index, thing in enumerate(top_things):
        logger.info(
            "#{} - {}: {:.2f} / intersection".format(
                index + 1,
                thing,
                mean_counts[thing],
            )
        )

    def date_of_object(object_name: str) -> datetime:
        try:
            return datetime.strptime(
                "-".join(object_name.split("-")[:6]),
                "%Y-%m-%d-%H-%M-%S",
            )
        except:
            return None

    dates = {
        object_name: date_of_object(object_name)
        for object_name in published_object_name
    }

    plt.figure(figsize=(15, 5))
    for thing in top_things:
        plt.semilogy(
            dates.values(),
            df[thing].values,
            label=f"{thing}: {mean_counts[thing]:.2f}",
        )

    plt.xlabel(
        " | ".join(
            [
                f"{len(published_object_name)} acquisition(s)",
                f"{NAME}-{VERSION}",
                fullname(),
            ]
        )
    )
    plt.ylabel("mean count / intersection")
    plt.grid(True)
    plt.title(
        " | ".join(
            [
                object_name,
            ]
        )
    )
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    file.save_fig(os.path.join(object_path, "counts.png"), log=True)

    return (
        post_to_object(
            object_name,
            "cache",
            {
                "mean_counts": mean_counts,
                "published_object_name": published_object_name,
            },
            verbose=verbose,
        )
        and file.save_csv(
            os.path.join(object_path, "counts.csv"),
            df,
            log=True,
        ),
        df,
    )
