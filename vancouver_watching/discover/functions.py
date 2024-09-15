from typing import List
import os
import requests
from tqdm import tqdm

from blueness import module
from blue_objects import file

from vancouver_watching import NAME
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


def discover_cameras_vancouver_style(filename: str, prefix: str) -> bool:
    from vancouver_watching.QGIS import label_of_camera
    from bs4 import BeautifulSoup

    logger.info(f"{NAME}.discover_cameras({filename}): vancouver-style")

    success, gdf = file.load_geodataframe(filename)
    if not success:
        return False

    list_of_cameras = []
    list_of_labels = []
    failed_locations = []
    for _, row in tqdm(gdf.iterrows()):
        list_of_cameras_ = []

        try:
            html_page = requests.get(row["url"])

            # https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948
            soup = BeautifulSoup(html_page.content, "html.parser")
            list_of_cameras_ = [
                f'{prefix}{item.attrs["src"]}'
                for item in soup.find(
                    "div",
                    class_="col-sm-12 section--container",
                ).findAll("img")
            ]
        except:
            failed_locations += [row["url"]]
            logger.error(f"failed: {row['url']}")

        list_of_cameras += [",".join(list_of_cameras_)]
        list_of_labels += [
            label_of_camera(
                row["url"],
                row["name"],
                list_of_cameras_,
            )
        ]
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

    gdf["cameras"] = list_of_cameras
    gdf["label"] = list_of_labels

    return file.save_geojson(filename, gdf)


def get_list_of_areas() -> List[str]:
    return [
        file.name(filename)
        for filename in file.list_of(
            os.path.join(
                file.path(__file__),
                "../.abcli/discovery/*.sh",
            )
        )
    ]
