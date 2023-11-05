import argparse
from vancouver_watching import VERSION
from vancouver_watching.ai import NAME, infer
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="infer",
)
parser.add_argument(
    "--filename",
    type=str,
    default="",
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
    "--model_id",
    type=str,
    default="",
)
args = parser.parse_args()

success = False
if args.task == "infer":
    success = infer(
        args.filename,
        args.model_id,
        args.do_dryrun,
        args.verbose,
    )
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
