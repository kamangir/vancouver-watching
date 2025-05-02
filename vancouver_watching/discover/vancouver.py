import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

from blueness import module
from bluer_objects import objects
from bluer_objects.metadata import post_to_object
from bluer_geo.file import load_geodataframe, save_geojson

from vancouver_watching import NAME
from vancouver_watching.QGIS import label_of_camera
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


def discover(
    object_name: str,
    prefix: str,
    count: int = -1,
) -> bool:
    logger.info(
        "{}.discover({}{}) -> {}".format(
            NAME,
            prefix,
            "" if count == -1 else f"count={count}",
            object_name,
        )
    )

    filename = objects.path_of(
        object_name=object_name,
        filename="detections.geojson",
    )

    success, gdf = load_geodataframe(filename)
    if not success:
        return False

    list_of_cameras = []
    list_of_labels = []
    failed_locations = []
    row_count = 0
    for _, row in tqdm(gdf.iterrows()):
        list_of_cameras_ = []

        try:
            html_page = requests.get(row["url"])

            # https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948
            soup = BeautifulSoup(html_page.content, "html.parser")

            list_of_cameras_ = [
                f"{prefix}{src}"
                for src in [img["src"] for img in soup.find_all("img")]
                if src.startswith("cameraimages")
            ]
        except Exception as e:
            failed_locations += [row["url"]]
            logger.error(f"failed: {e}: {row['url']}")

        list_of_cameras += [",".join(list_of_cameras_)]
        list_of_labels += [
            label_of_camera(
                row["url"],
                row["name"],
                list_of_cameras_,
            )
        ]

        row_count += 1
        if count != -1 and row_count >= count:
            break

    if failed_locations:
        logger.error(f"{len(failed_locations)} location(s) failed.")
    logger.info(
        "found {} camera(s) in {} location(s).".format(
            len(
                [camera for camera in (",".join(list_of_cameras)).split(",") if camera]
            ),
            len(gdf),
        )
    )

    # for safety when count != -1
    gdf["cameras"] = (list_of_cameras + [""] * len(gdf))[: len(gdf)]
    gdf["label"] = (list_of_labels + [""] * len(gdf))[: len(gdf)]

    if not save_geojson(filename, gdf):
        return False

    return post_to_object(
        object_name,
        "discovery",
        {
            "target": "vancouver",
            "cameras": len(list_of_cameras),
            "locations": len(gdf),
        },
    )
