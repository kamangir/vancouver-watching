from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from abcli import file
from . import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_geojson(filename):
    logger.info(f"{NAME}.ingest_geojson({filename})")

    success, content = file.load_geojson(filename)
    if not success:
        return success

    for feature in tqdm(content["features"]):
        url = feature["properties"]["url"]

        html_page = requests.get(url)

        # https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948
        soup = BeautifulSoup(html_page.content, "html.parser")

    return True
