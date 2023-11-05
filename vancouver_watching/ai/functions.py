from abcli import file
from vancouver_watching.ai import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def run_model(
    metadata_filename: str,
    model_id: str,
    do_dryrun: bool = False,
):
    success, metadata = file.load_json(metadata_filename)
    if not success:
        return False
    logger.info(
        "{}.ingest_from_cameras: {} image(s) from {} -{}->".format(
            NAME,
            len(metadata),
            metadata_filename,
            model_id,
        )
    )

    logger.info("🪄")

    return True
