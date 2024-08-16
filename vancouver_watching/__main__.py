from vancouver_watching import NAME, VERSION, DESCRIPTION, ICON
from vancouver_watching.logger import logger
from blueness.argparse.generic import main

success, message = main(
    __file__,
    NAME,
    VERSION,
    DESCRIPTION,
    ICON,
)
if not success:
    logger.error(message)
