import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from vancouver_watching import NAME
from vancouver_watching.discover.targets import get_list_of_targets
from vancouver_watching.discover.vancouver import discover as discover_vancouver
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help="vancouver | list_of_targets",
)
parser.add_argument(
    "--object_name",
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
parser.add_argument(
    "--count",
    type=int,
    default="-1",
    help="-1 for all",
)
args = parser.parse_args()

delim = " " if args.delim == "space" else args.delim

success = False
if args.task == "list_of_targets":
    print(delim.join(get_list_of_targets()))
    success = True
elif args.task == "vancouver":
    success = discover_vancouver(
        object_name=args.object_name,
        prefix=args.prefix,
        count=args.count,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
