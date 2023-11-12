import argparse
from vancouver_watching import VERSION
from vancouver_watching.area import Area
from vancouver_watching.ai import NAME
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="process",
)
parser.add_argument(
    "--geojson",
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
    "--verbose",
    type=int,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--overwrite",
    type=int,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--model_id",
    type=str,
    default="",
)
args = parser.parse_args()

success = False
if args.task == "process":
    area = Area(
        args.geojson,
        do_dryrun=args.do_dryrun,
        verbose=args.verbose,
    )
    success = area.valid

    if success:
        success = area.detect_objects(
            model_id=args.model_id,
            overwrite=args.overwrite,
        )

else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
