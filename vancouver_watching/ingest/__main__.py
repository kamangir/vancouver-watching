import argparse
from vancouver_watching import VERSION
from vancouver_watching.ingest import NAME, ingest_from_cameras
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="from_cameras",
)
parser.add_argument(
    "--filename",
    type=str,
    default="",
)
parser.add_argument(
    "--do_dryrun",
    type=int,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--count",
    type=int,
    default=-1,
)
args = parser.parse_args()

success = False
if args.task == "from_cameras":
    success = ingest_from_cameras(
        args.filename,
        args.count,
        args.do_dryrun,
    )
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
