import argparse
from vancouver_watching import VERSION
from vancouver_watching.area import Area
from vancouver_watching.ingest import NAME
from vancouver_watching.logger import logger


parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "--geojson",
    type=str,
    default="",
)
parser.add_argument(
    "--count",
    type=int,
    default=-1,
)
parser.add_argument(
    "--do_dryrun",
    type=int,
    default=0,
    help="0|1",
)
args = parser.parse_args()

area = Area(
    args.geojson,
    do_dryrun=args.do_dryrun,
)
success = area.valid

if success:
    success = area.ingest(count=args.count)

if not success:
    logger.error(f"{args.task}: failed.")
