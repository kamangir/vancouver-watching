import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from vancouver_watching import NAME
from vancouver_watching.target import Target
from vancouver_watching.target.detection import detect_in_target
from vancouver_watching.target.ingest import ingest_target
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)

list_of_tasks = ["detect", "ingest"]

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help=" | ".join(list_of_tasks),
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
    "--model_id",
    type=str,
    default="",
)
args = parser.parse_args()

success = args.task in list_of_tasks

if success:
    target = Target(
        map_filename=args.geojson,
        do_dryrun=args.do_dryrun,
        verbose=args.verbose,
    )
    success = target.valid

if args.task == "detect":
    if success:
        success = detect_in_target(
            target=target,
            model_id=args.model_id,
            animated_gif=args.animated_gif,
            count=args.count,
            overwrite=args.overwrite,
        )
elif args.task == "ingest":
    if success:
        success = ingest_target(
            target=target,
            count=args.count,
        )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
