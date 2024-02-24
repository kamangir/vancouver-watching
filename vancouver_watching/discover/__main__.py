import argparse
from vancouver_watching import VERSION
from vancouver_watching.discover import NAME
from vancouver_watching.discover.functions import (
    discover_cameras_vancouver_style,
    get_list_of_areas,
)
from vancouver_watching.logger import logger


parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
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
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
