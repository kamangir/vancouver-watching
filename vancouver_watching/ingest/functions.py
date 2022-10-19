from bs4 import BeautifulSoup
import geopandas
import os
import os.path
import requests
from tqdm import tqdm
from abcli import file
from . import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def get_list_of_cameras(filename):
    logger.info(f"{NAME}.get_list_of_cameras({filename})")

    gdf = geopandas.read_file(filename)

    if "cameras" in gdf.columns:
        logger.info('vancouver_watching: get_list_of_cameras: "cameras" found.')
        list_of_cameras = list(gdf["cameras"])
    else:
        list_of_cameras = []
        list_of_labels = []
        err_count = 0
        for index, row in tqdm(gdf.iterrows()):
            list_of_cameras_ = []

            try:
                html_page = requests.get(row["url"])

                # https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948
                soup = BeautifulSoup(html_page.content, "html.parser")
                list_of_cameras_ = [
                    item.attrs["src"]
                    for item in soup.find(
                        "div",
                        class_="col-sm-12 section--container",
                    ).findAll("img")
                ]
            except:
                err_count += 1
                logger.error(f"failed: {row['url']}")

            list_of_cameras += [",".join(list_of_cameras_)]
            list_of_labels += [
                '<a href="{}">{}</a><br/> {}'.format(
                    row["url"],
                    row["name"],
                    "<br/> ".join(
                        [
                            f'<img src="https://trafficcams.vancouver.ca/{image}">'
                            for image in list_of_cameras_
                        ]
                    ),
                )
            ]

        gdf["cameras"] = list_of_cameras
        gdf["label"] = list_of_labels

        gdf.to_file(filename, driver="GeoJSON")

    list_of_cameras = [
        camera for camera in (",".join(list_of_cameras)).split(",") if camera
    ]

    logger.info(f"found {len(list_of_cameras)} camera(s)")

    return list_of_cameras


def ingest_from_cameras(filename):
    list_of_cameras = get_list_of_cameras(filename)

    logger.info(
        f"{NAME}.ingest_geojson({filename}): ingesting from {len(list_of_cameras)} cameras(s)."
    )

    success = True
    for camera in tqdm(list_of_cameras):
        if not file.download(
            f"https://trafficcams.vancouver.ca/{camera}",
            os.path.join(
                os.getenv("abcli_object_path"),
                file.name_and_extension(camera),
            ),
        ):
            success = False

    return success
