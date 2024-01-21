import argparse
from vancouver_watching import NAME, VERSION, DESCRIPTION
from vancouver_watching.QGIS import update_cache
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="update_cache|version",
)
parser.add_argument(
    "--show_description",
    type=bool,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--object_name",
    type=str,
    default=".",
)
args = parser.parse_args()

success = False
if args.task == "update_cache":
    success = update_cache(args.object_name)
elif args.task == "version":
    print(
        "{}-{}{}".format(
            NAME,
            VERSION,
            "\\n{}".format(DESCRIPTION) if args.show_description else "",
        )
    )
    success = True
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
