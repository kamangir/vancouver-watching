from bs4 import BeautifulSoup
import geopandas
import requests
from tqdm import tqdm
from . import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def digest_geojson(filename, prefix):
    logger.info(f"{NAME}.digest_geojson({filename})")

    gdf = geopandas.read_file(filename)

    list_of_cameras = []
    list_of_labels = []
    failed_cameras = []
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
            failed_cameras += [row["url"]]
            logger.error(f"failed: {row['url']}")

        if failed_cameras:
            logger.error(f"{len(failed_cameras)} error(s): {', '.join(failed_cameras)}")

        list_of_cameras += [",".join(list_of_cameras_)]
        list_of_labels += [
            '<a href="{}">{}</a><br/> {}'.format(
                row["url"],
                row["name"],
                "<br/> ".join([f'<img src="{camera}">' for camera in list_of_cameras_]),
            )
        ]

    gdf["cameras"] = list_of_cameras
    gdf["label"] = list_of_labels

    gdf.to_file(filename, driver="GeoJSON")

    list_of_cameras = [
        camera for camera in (",".join(list_of_cameras)).split(",") if camera
    ]
    logger.info(f"found {len(list_of_cameras)} camera(s)")

    return True


def get_list_of_cameras(filename, log=True):
    gdf = geopandas.read_file(filename)

    if "cameras" not in gdf.columns:
        return False, []

    output = [
        camera for camera in (",".join(list(gdf["cameras"]))).split(",") if camera
    ]

    if log:
        logger.info(f"found {len(output)} camera(s)")

    return True, output
