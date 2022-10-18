from . import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_geojson(filename):
    logger.info(f"{NAME}.ingest_geojson({filename})")

    return True
