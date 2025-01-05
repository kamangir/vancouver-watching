from typing import List

from blue_options.terminal import show_usage, xtra
from abcli.help.generic import help_functions as generic_help_functions

from vancouver_watching import ALIAS
from vancouver_watching.help.discover import help_discover
from vancouver_watching.help.ingest import help_ingest
from vancouver_watching.help.process import help_process
from vancouver_watching.help.update_cache import help_update_cache


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "discover": help_discover,
        "ingest": help_ingest,
        "process": help_process,
        "update_cache": help_update_cache,
    }
)
