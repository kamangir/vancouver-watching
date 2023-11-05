import argparse
from vancouver_watching import VERSION
from vancouver_watching.analysis import NAME, analyze_object
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="analyze",
)
parser.add_argument(
    "--object_path",
    type=str,
    default="",
)
args = parser.parse_args()

success = False
if args.task == "analyze":
    success = analyze_object(args.object_path)
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
