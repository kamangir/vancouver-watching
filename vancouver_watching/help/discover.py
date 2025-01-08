from typing import List

from blue_options.terminal import show_usage, xtra

from vancouver_watching.discover.functions import get_list_of_targets

target_details = {
    "target: {}".format(" | ".join(get_list_of_targets())): [],
}


def help_discover(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "target=<target>",
            xtra(",count=<-1>,dryrun,~tag,~upload", mono=mono),
        ]
    )

    return show_usage(
        [
            "vanwatch",
            "discover",
            f"[{options}]",
            "[-|<object-name>]",
            "[<args>]",
        ],
        "discover <target> -> <object-name>.",
        target_details,
        mono=mono,
    )
