import argparse
from vancouver_watching import NAME, VERSION, DESCRIPTION, ICON
from vancouver_watching.logger import logger
from vancouver_watching.QGIS import update_cache

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="update_cache|version",
)
parser.add_argument(
    "--object_name",
    type=str,
    default=".",
)
parser.add_argument(
    "--show_description",
    type=int,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--show_icon",
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
args = parser.parse_args()

success = False
if args.task == "locate":
    success = True
    print(__file__)
elif args.task == "update_cache":
    success, _ = update_cache(
        object_name=args.object_name,
        verbose=args.verbose,
    )
elif args.task == "version":
    print(
        "{}{}-{}{}".format(
            f"{ICON} " if args.show_icon else "",
            NAME,
            VERSION,
            "\\n{}".format(DESCRIPTION) if args.show_description else "",
        )
    )
    success = True
else:
    logger.error(f"{args.task}: command not found.")

if not success:
    logger.error(f"{args.task}: failed.")
