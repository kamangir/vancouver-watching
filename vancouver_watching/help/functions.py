from typing import List

from blue_options.terminal import show_usage, xtra
from abcli.help.generic import help_functions as generic_help_functions

from vancouver_watching import ALIAS
from vancouver_watching.help.discover import help_discover
from vancouver_watching.help.ingest import help_ingest
from vancouver_watching.help.detect import help_detect


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "detect": help_detect,
        "discover": help_discover,
        "ingest": help_ingest,
    }
)
