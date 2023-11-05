from vancouver_watching.analysis import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def analyze_object(object_path):
    logger.info("{}.analyze_object: {}".format(NAME, object_path))

    logger.info("🪄")

    return True
