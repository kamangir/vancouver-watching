from blueness import module
from bluer_objects import objects, file
from bluer_geo.file import load_geodataframe

from vancouver_watching import NAME
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


def test(object_name: str) -> bool:
    filename = objects.path_of(
        object_name=object_name,
        filename="detections.geojson",
    )

    logger.info(f"{NAME}.test({object_name}): {filename}")

    success, gdf = load_geodataframe(filename)
    if not success:
        logger.error("can not load detections.geojson!")
        return False
    logger.info("✅ loaded detections.geojson.")

    for column_name in [
        "cameras",
        "label",
        "mapid",
    ]:
        if column_name not in gdf.columns:
            logger.error(f"{column_name} not in detections.geojson!")
            return False
        logger.info(f"✅ {column_name} in detections.geojson.")

    return True
