import argparse

from blueness import module
from blueness.argparse.generic import sys_exit

from vancouver_watching import NAME
from vancouver_watching.discover.targets import list_of_targets
from vancouver_watching.discover.vancouver import discover as discover_vancouver
from vancouver_watching.discover.toronto import toronto as discover_toronto
from vancouver_watching.discover.testing import test as test_discovery
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help=" | ".join(
        sorted(
            [
                "list_of_targets",
                "test",
            ]
            + list_of_targets()
        )
    ),
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
if args.task == "list_targets":
    print(delim.join(list_of_targets()))
    success = True
elif args.task == "test":
    success = test_discovery(
        object_name=args.object_name,
    )
elif args.task == "vancouver":
    success = discover_vancouver(
        object_name=args.object_name,
        prefix=args.prefix,
        count=args.count,
    )
elif args.task == "toronto":
    success = discover_toronto(
        object_name=args.object_name,
        prefix=args.prefix,
        count=args.count,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
