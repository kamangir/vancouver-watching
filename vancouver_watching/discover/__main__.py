import argparse
from . import *
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="discover_cameras",
)
parser.add_argument(
    "--filename",
    type=str,
    default="",
)
args = parser.parse_args()

success = False
if args.task == "discover_cameras":
    success = discover_cameras(args.filename)
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
