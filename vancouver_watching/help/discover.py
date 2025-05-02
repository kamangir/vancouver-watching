from typing import List

from bluer_options.terminal import show_usage, xtra

from vancouver_watching.discover.targets import list_of_targets

target_details = {
    "target: {}".format(" | ".join(list_of_targets())): [],
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
