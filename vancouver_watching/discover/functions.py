import os
import requests
from tqdm import tqdm
from abcli import file
from . import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def discover_cameras_vancouver_style(filename, prefix):
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


def get_list_of_areas():
    return [
        file.name(filename)
        for filename in file.list_of(
            os.path.join(
                os.getenv("abcli_path_git", ""),
                "Vancouver-Watching/.abcli/discovery/*.sh",
            )
        )
    ]


def get_list_of_cameras(filename, log=True):
    import geopandas

    gdf = geopandas.read_file(filename)

    if "cameras" not in gdf.columns:
        return False, []

    output = [
        camera for camera in (",".join(list(gdf["cameras"]))).split(",") if camera
    ]

    if log:
        logger.info(f"found {len(output)} camera(s)")

    return True, output
