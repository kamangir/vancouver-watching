import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from vancouver_watching import NAME
from vancouver_watching.area import Area
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
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
    "--count",
    type=int,
    default=-1,
    help="-1: all",
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
    "--animated_gif",
    type=int,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--detect_objects",
    type=int,
    default=1,
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

    if success and args.detect_objects:
        success = area.detect_objects(
            model_id=args.model_id,
            animated_gif=args.animated_gif,
            count=args.count,
            overwrite=args.overwrite,
        )

    if success:
        success = area.summarize()
else:
    success = None

sys_exit(logger, NAME, args.task, success)
