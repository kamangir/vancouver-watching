import argparse
from . import *
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="digest_geojson",
)
parser.add_argument(
    "--filename",
    type=str,
    default="",
)
parser.add_argument(
    "--prefix",
    type=str,
    default="",
)
args = parser.parse_args()

success = False
if args.task == "digest_geojson":
    success = digest_geojson(
        args.filename,
        args.prefix,
    )
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
