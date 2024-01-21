import os
from datetime import datetime
import glob
from abcli import file
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


def update_cache(
    object_name: str = ".",
    verbose: bool = False,
) -> bool:
    logger.info(f"update_cache({object_name})")

    object_path = objects.object_path(object_name, create=True)

    published_object_name = sorted(
        [
            file.name(filename)
            for filename in glob.glob(os.path.join(object_path, "*.geojson"))
        ]
    )
    logger.info(
        "🌀 {} geojson(s) found{}".format(
            len(published_object_name),
            ": {}".format(", ".join(published_object_name)) if verbose else ".",
        )
    )

    acquisition_day = {
        object_name: datetime.strptime(
            "-".join(object_name.split("-")[:6]),
            "%Y-%m-%d-%H-%M-%S",
        )
        for object_name in published_object_name
    }

    print(acquisition_day)

    for object_name in published_object_name:
        filename = os.path.join(object_path, f"{object_name}.geojson")
        logger.info(f"🌀 {filename}")

        success, gdf = file.load_geodataframe(filename)
        if not success:
            continue

        print(gdf.columns)
        break

    # TODO: acquisition count per day

    # TODO: object count per day

    return True
