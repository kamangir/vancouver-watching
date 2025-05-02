from blueness import module
from bluer_objects import objects, file

from vancouver_watching import NAME
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


def test(object_name: str) -> bool:
    logger.info(f"{NAME}.test({object_name})")

    filename = objects.path_of(
        object_name=object_name,
        filename="detections.geojson",
    )
    if not file.exists(filename):
        logger.error(f"{filename} does not exist!")
        return False
    logger.info(f"✅ {filename}")

    logger.info("🪄")

    return True
