import os
import glob
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


def update_cache(object_name: str = ".") -> bool:
    logger.info(f"update_cache({object_name})")

    object_path = objects.object_path(object_name, create=True)

    for filename in glob.glob(os.path.join(object_path, "*.geojson")):
        logger.info(f"🌀 {filename}")
    return True
