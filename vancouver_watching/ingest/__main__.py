import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from vancouver_watching import NAME
from vancouver_watching.target import Target
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
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

target = Target(
    args.geojson,
    do_dryrun=args.do_dryrun,
)
success = target.valid

if success:
    success = target.ingest(count=args.count)


sys_exit(logger, NAME, "ingest", success)
