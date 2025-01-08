from typing import List

from blue_options.terminal import show_usage, xtra

from vancouver_watching.help.discover import target_details
from vancouver_watching.help.detect import (
    args as detect_args,
    options as detect_options,
)


def help_ingest(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "target=<target>",
            xtra(",count=<-1>,~download,dryrun,~upload", mono=mono),
        ]
    )

    return show_usage(
        [
            "vanwatch",
            "ingest",
            f"[{options}]",
            "[-|<object-name>]",
            f"[detect,{detect_options(mono=mono)}]",
        ]
        + detect_args,
        "ingest <target> -> <object-name>.",
        target_details,
        mono=mono,
    )
