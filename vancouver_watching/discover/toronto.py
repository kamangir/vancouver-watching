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


def toronto(
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

    logger.info("🪄")

    return post_to_object(
        object_name,
        "discovery",
        {
            "cameras": 0,
            "locations": 0,
        },
    )
