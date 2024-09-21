import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from vancouver_watching import NAME
from vancouver_watching.discover.functions import (
    discover_cameras_vancouver_style,
    get_list_of_areas,
)
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="discover_cameras_vancouver_style|list_of_areas",
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
parser.add_argument(
    "--delim",
    type=str,
    default="+",
)
args = parser.parse_args()

delim = " " if args.delim == "space" else args.delim

success = False
if args.task == "list_of_areas":
    print(delim.join(get_list_of_areas()))
    success = True
elif args.task == "discover_cameras_vancouver_style":
    success = discover_cameras_vancouver_style(
        args.filename,
        args.prefix,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
