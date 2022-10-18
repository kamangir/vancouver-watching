from bs4 import BeautifulSoup
import geopandas
import requests
from tqdm import tqdm
from abcli import file
from . import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_geojson(filename):
    logger.info(f"{NAME}.ingest_geojson({filename})")

    gdf = geopandas.read_file(filename)

    list_of_images = []
    list_of_labels = []
    camera_count = 0
    err_count = 0
    for index, row in tqdm(gdf.iterrows()):
        list_of_images_ = []

        try:
            html_page = requests.get(row["url"])

            # https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948
            soup = BeautifulSoup(html_page.content, "html.parser")
            list_of_images_ = [
                item.attrs["src"]
                for item in soup.find(
                    "div",
                    class_="col-sm-12 section--container",
                ).findAll("img")
            ]
        except:
            err_count += 1
            logger.error(f"-vancouver_watching: ingest: {row['url']} failed.")

        camera_count += len(list_of_images_)

        list_of_images += [",".join(list_of_images_)]
        list_of_labels += [
            '<a href="{}">{}</a><br/> {}'.format(
                row["url"],
                row["name"],
                "<br/> ".join(
                    [
                        f'<img src="https://trafficcams.vancouver.ca/{image}">'
                        for image in list_of_images_
                    ]
                ),
            )
        ]

    gdf["images"] = list_of_images
    gdf["label"] = list_of_labels

    gdf.to_file(filename, driver="GeoJSON")

    logger.info(f"total number of cameras: {camera_count}")

    return True
