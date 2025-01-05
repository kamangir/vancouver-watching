from typing import List

from blue_options.terminal import show_usage, xtra
from abcli.help.generic import help_functions as generic_help_functions

from vancouver_watching.help.discover import area_details
from vancouver_watching.help.process import (
    args as process_args,
    options as process_options,
)


def help_ingest(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "area=<area>",
            xtra(",count=<-1>,~download,dryrun,~upload", mono=mono),
        ]
    )

    return show_usage(
        [
            "vanwatch",
            "ingest",
            f"[{options}]",
            "[-|<object-name>]",
            f"[process,{process_options(mono=mono)}]",
        ]
        + process_args,
        "ingest <area> -> <object-name>.",
        area_details,
        mono=mono,
    )
